from flask import Flask, render_template, session
from werkzeug.middleware.proxy_fix import ProxyFix

# Blueprint importieren
from controller.user_controller import user_bp
from controller.product_controller import product_bp
from controller.cart_controller import cart_bp


app = Flask(__name__, template_folder='templates')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
app.secret_key = 'ein_ganz_geheimer_schluessel'

# Blueprint registrieren
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)

app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    PERMANENT_SESSION_LIFETIME=1800 # 30 Minuten Haltbarkeit
)

if __name__ == "__main__":
    app.run(debug=True)