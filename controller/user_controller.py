from flask import Blueprint, render_template, request, redirect, url_for, session
from database.db_manager import DB_Manager
from model.customer.customer import Customer

# Blueprint definieren
user_bp = Blueprint('user', __name__)

@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_from_form = request.form.get('email')
        password_from_form = request.form.get('password')

        db = DB_Manager()
        user = db.check_login(email_from_form, password_from_form)

        if user:
            session["user_id"] = str(user.id)
            session["user_name"] = user.name
            return redirect(url_for("product.index"))

        return render_template("login.html", error="Ungültige Zugangsdaten")

    return render_template("login.html")

@user_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        mail = request.form.get('email')
        password = request.form.get('password')
        tel = request.form.get('tel', '')
        addr = request.form.get('address', '')
        geb = request.form.get('geb_date', None)

        # Neues Customer-Objekt erstellen
        new_customer = Customer(None, mail, tel, name, addr, geb, None)

        db = DB_Manager()
        db.save_entity(new_customer, password)

        # Nach Registrierung zum Login (innerhalb dieses Blueprints)
        return redirect(url_for('user.login'))

    return render_template("register.html")

@user_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("product.index"))