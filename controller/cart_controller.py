from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db_manager import DB_Manager
from model.product.book import Book
from model.product.clothes import Clothes
from model.product.electronic import Electronic
from model.shopping_cart.shopping_cart import Shopping_Cart

cart_bp = Blueprint('cart', __name__)


@cart_bp.route("/add_to_cart", methods=['POST'])
def add_to_cart():
    p_id = request.form.get('p_id')
    user_id = session.get('user_id')

    if not user_id:
        flash("Bitte logge dich ein, um Artikel in den Warenkorb zu legen.", "warning")
        return redirect(url_for('user.login'))

    db = DB_Manager()
    product = None

    try:
        # Suche in allen Produktkategorien (da p_id eindeutig sein sollte)
        # Wir nutzen hier p.product_id, passend zu deinem SQL in den Models
        search_results = []
        search_results.extend(db.search_entities(Book, "p.product_id", p_id))
        search_results.extend(db.search_entities(Electronic, "p.product_id", p_id))
        search_results.extend(db.search_entities(Clothes, "p.product_id", p_id))

        if search_results:
            product = search_results[0]
            # Hier käme die Logik zum Speichern in der DB oder Session
            # Da Shopping_Cart noch fehlt, hier als Platzhalter für die DB-Aktion:
            # db.add_item_to_cart_table(user_id, product.product_id)
            flash(f"'{product.name}' wurde zum Warenkorb hinzugefügt!", "success")
        else:
            flash("Produkt konnte nicht gefunden werden.", "danger")

    except Exception as e:
        flash(f"Fehler beim Hinzufügen: {str(e)}", "danger")

    return redirect(url_for('product.index'))


@cart_bp.route("/cart")
def show_cart():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('user.login'))

    db = DB_Manager()
    # Da wir Shopping_Cart noch nicht final haben, laden wir die Items über den DB_Manager
    cart_items = db.get_cart_items(user_id)

    # Dummy-Kunde für das Template (sollte eigentlich aus der Session/DB kommen)
    from model.customer.private_customer import Private_Customer
    current_customer = Private_Customer(user_id, session.get('user_email'), "", session.get('user_name'), "", "")

    # Erstellung des Cart-Objekts für das Template
    cart = Shopping_Cart(current_customer)
    for item in cart_items:
        cart.add_item(item)

    return render_template("cart.html", cart=cart)


@cart_bp.route("/checkout", methods=['POST'])
def checkout():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('user.login'))

    db = DB_Manager()
    cart_items = db.get_cart_items(user_id)

    if not cart_items:
        flash("Dein Warenkorb ist leer!", "info")
        return redirect(url_for('cart.show_cart'))

    # Warenkorb-Logik für den Checkout
    from model.customer.private_customer import Private_Customer
    current_customer = Private_Customer(user_id, "", "", session.get('user_name'), "", "")
    new_cart = Shopping_Cart(current_customer)
    for item in cart_items:
        new_cart.add_item(item)

    order_id = db.save_order(new_cart)

    if order_id:
        return render_template("checkout_success.html", order_id=order_id)
    else:
        flash("Fehler beim Abschließen der Bestellung.", "danger")
        return redirect(url_for('cart.show_cart'))