from flask import Flask, render_template, session

# Blueprint importieren
from controller.user_controller import user_bp
from controller.product_controller import product_bp


app = Flask(__name__, template_folder='templates')
app.secret_key = 'ein_ganz_geheimer_schluessel'

# Blueprint registrieren
app.register_blueprint(user_bp)

app.register_blueprint(product_bp)

if __name__ == "__main__":
    app.run(debug=True)