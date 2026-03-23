from flask import Flask, render_template, request, redirect, url_for, session
from database.db_manager import DB_Manager
from model.product.book import Book

app = Flask(__name__, template_folder='.')
app.secret_key = 'ein_ganz_geheimer_schluessel'


@app.route("/")
@app.route("/category/<cat>")
def index(cat=None):
    db = DB_Manager()

    if cat == "books":
        products = db.load_entities(Book)
    else:
        products = db.load_entities(Book)

    return render_template("index.html", products=products, category=cat)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        db = DB_Manager()
        user = db.check_login(email, password)

        if user:
            session["user_id"] = user.id
            session["user_name"] = user.name
            return redirect(url_for("index"))

        return render_template("login.html", error="Ungültige Zugangsdaten")

    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        from model.customer.customer import Customer
        new_customer = Customer(None, name, email, password)

        db = DB_Manager()
        db.save_entity(new_customer)

        return redirect(url_for('login'))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)