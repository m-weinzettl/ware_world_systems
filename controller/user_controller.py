from flask import Blueprint, render_template, request, redirect, url_for, session
from database.db_manager import DB_Manager
from model.customer.customer import Customer
from model.validator import Validator
from werkzeug.security import generate_password_hash

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

        # 1. Validierung (Stärke prüfen)
        is_valid, result = Validator.validate_password(password)
        if not is_valid:
            return render_template("register.html", error=result)

        # 2. Hashing (Standard-Einstellungen nutzen)
        hashed_password = generate_password_hash(password)

        # 3. Customer-Objekt erstellen
        new_customer = Customer(None, mail, tel, name, addr, geb, None)

        # 4. Speichern (WICHTIG: hashed_password übergeben!)
        db = DB_Manager()
        db.save_entity(new_customer, hashed_password)

        return redirect(url_for('user.login'))

    return render_template("register.html")

@user_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("product.index"))