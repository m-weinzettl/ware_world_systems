from flask import Flask, render_template, request, redirect, url_for, session
from database.db_manager import DB_Manager
from model.product.book import Book
from model.product.clothes import Clothes
from model.product.electronic import Electronic

app = Flask(__name__, template_folder='.')
app.secret_key = 'ein_ganz_geheimer_schluessel'


@app.route("/")
@app.route("/category/<cat>")
def index(cat=None):
    db = DB_Manager()

    current_cat = cat if cat else "books"

    category_map = {
        "books": Book,
        "clothes": Clothes,
        "electronic": Electronic,
    }

    product_class = category_map.get(cat, Book)
    products = db.load_entities(product_class)


    return render_template("index.html", products=products, category=current_cat)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_from_form = request.form.get('email')
        password_from_form = request.form.get('password')

        db = DB_Manager()
        user = db.check_login(email_from_form, password_from_form)

        if user:
            session["user_id"] = str(user.id)
            session["user_name"] = user.name
            return redirect(url_for("index"))

        return render_template("login.html", error="Ungültige Zugangsdaten")

    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        mail = request.form.get('email')
        password = request.form.get('password')
        # Falls Geburtsdatum oder Adresse im Formular, hier holen:
        tel = request.form.get('tel', '')
        addr = request.form.get('address', '')
        geb = request.form.get('geb_date', None)

        from model.customer.customer import Customer
        # WICHTIG: Alle 7 Parameter übergeben (id, mail, tel, name, addr, geb, uid)
        new_customer = Customer(None, mail, tel, name, addr, geb, None)

        db = DB_Manager()
        # Password muss separat an save_entity übergeben werden,
        # da es nicht im Customer-Objekt gespeichert wird (laut Logik)
        db.save_entity(new_customer, password)

        return redirect(url_for('login'))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)