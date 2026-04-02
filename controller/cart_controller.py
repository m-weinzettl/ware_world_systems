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
    customer_id = session.get('customer_id')

    if not customer_id:
        flash("Bitte logge dich ein, um Artikel in den Warenkorb zu legen.", "warning")
        return redirect(url_for('user.login'))

    db = DB_Manager()

    try:
        # 1. Wir prüfen erst, ob das Produkt existiert (Validierung)
        search_results = []
        search_results.extend(db.search_entities(Book, "p.product_id", p_id))
        search_results.extend(db.search_entities(Electronic, "p.product_id", p_id))
        search_results.extend(db.search_entities(Clothes, "p.product_id", p_id))

        if search_results:
            product = search_results[0]
            # 2. ECHTE DB-AKTION: In die shopping_cart Tabelle schreiben
            success = db.add_item_to_cart(customer_id, product.product_id)

            if success:
                flash(f"'{product.name}' wurde zum Warenkorb hinzugefügt!", "success")
            else:
                flash("Fehler beim Speichern im Warenkorb.", "danger")
        else:
            flash("Produkt konnte nicht gefunden werden.", "danger")

    except Exception as e:
        flash(f"Systemfehler: {str(e)}", "danger")

    return redirect(url_for('product.index'))

@cart_bp.route("/remove_from_cart", methods=['POST'])
def remove_from_cart():
    p_id = request.form.get('p_id')
    customer_id = session.get('customer_id')

    if not customer_id:
        flash("Bitte logge dich ein, um Artikel aus dem Warenkorb zu entfernen.", "warning")
        return redirect(url_for('user.login'))

    db = DB_Manager()

    try:
        success = db.remove_item_from_cart(customer_id, p_id)

        if success:
            flash("Artikel wurde aus dem Warenkorb entfernt!", "success")
        else:
            flash("Fehler beim Entfernen des Artikels.", "danger")

    except Exception as e:
        flash(f"Systemfehler: {str(e)}", "danger")

    return redirect(url_for('cart.show_cart'))

@cart_bp.route("/cart")
def show_cart():
    customer_id = session.get('customer_id')
    if not customer_id:
        return redirect(url_for('user.login'))

    db = DB_Manager()
    # Holt die echten Produkte + Mengen aus der shopping_cart Tabelle
    cart_items = db.get_cart_items(customer_id)

    # Wir nutzen die Session-Daten, um das Customer-Objekt für den Warenkorb zu bauen
    # user_email muss im user_controller gesetzt sein!
    from model.customer.private_customer import Private_Customer
    current_customer = Private_Customer(
        customer_id=customer_id,
        mail=session.get('user_email', ''),
        tel_number="",
        name=session.get('user_name', 'Kunde'),
        address=session.get('user_address', ''),
        geb_date=None
    )

    cart = Shopping_Cart(current_customer)
    for item in cart_items:
        cart.add_item(item)

    return render_template("cart.html", cart=cart)

@cart_bp.route("/checkout", methods=['POST'])
def checkout():
    customer_id = session.get('customer_id')
    if not customer_id:
        return redirect(url_for('user.login'))

    db = DB_Manager()
    cart_items = db.get_cart_items(customer_id)

    if not cart_items:
        flash("Dein Warenkorb ist leer!", "info")
        return redirect(url_for('cart.show_cart'))

    from model.customer.private_customer import Private_Customer
    current_customer = Private_Customer(
        customer_id,
        session.get('user_mail', ''),
        "",
        session.get('user_name', 'Kunde'),
        "",
        ""
    )

    new_cart = Shopping_Cart(current_customer)
    for item in cart_items:
        new_cart.add_item(item)

    order_id = db.save_order(new_cart)

    if order_id:
        return render_template("checkout_success.html", order_id=order_id)
    else:
        flash("Fehler beim Abschließen der Bestellung.", "danger")
        return redirect(url_for('cart.show_cart'))

@cart_bp.route("/my_orders")
def my_orders():
    customer_id = session.get('customer_id')
    if not customer_id:
        return redirect(url_for('user.login'))
    db = DB_Manager()
    orders = db.get_orders_per_customer(customer_id)
    return render_template("my_orders.html", orders=orders)


@cart_bp.route("/download_invoice/<order_id>")
def download_invoice(order_id):
    customer_id = session.get('customer_id')
    if not customer_id:
        return redirect(url_for('user.login'))

    db = DB_Manager()
    invoice_data = db.get_invoice_data(order_id)

    if not invoice_data:
        flash("Rechnungsdaten konnten nicht gefunden werden.", "danger")
        return redirect(url_for('cart.my_orders'))

    import io
    from flask import send_file
    from controller.pdf_generator import Invoice_To_PDF  # Pfad ggf. anpassen

    # PDF generieren mit deiner Invoice_To_PDF Klasse
    pdf_gen = Invoice_To_PDF(invoice_data)
    # create_invoice_to_pdf(None) liefert laut deinem Code die Bytes (dest='S')
    pdf_bytes = pdf_gen.create_invoice_to_pdf(None)

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"Rechnung_{order_id}.pdf"
    )



