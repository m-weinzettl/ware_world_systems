from flask import Blueprint, render_template, request
from database.db_manager import DB_Manager
from model.product.book import Book
from model.product.clothes import Clothes
from model.product.electronic import Electronic

# Blueprint für Produkte erstellen
product_bp = Blueprint('product', __name__)


@product_bp.route("/")
@product_bp.route("/category/<cat>")
def index(cat=None):
    db = DB_Manager()

    # Standardmäßig "books", wenn nichts angegeben ist
    current_cat = cat if cat else "books"

    category_map = {
        "books": Book,
        "clothes": Clothes,
        "electronic": Electronic,
    }

    # Nutze current_cat für das Mapping
    product_class = category_map.get(current_cat, Book)
    products = db.load_entities(product_class)

    return render_template("index.html", products=products, category=current_cat)