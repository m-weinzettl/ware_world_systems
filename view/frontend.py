from flask import Flask, render_template
from database.db_manager import DB_Manager
from model.product.book import Book

# Da index.html im gleichen Ordner wie frontend.py liegt (view/)
app = Flask(__name__, template_folder='.')

@app.route("/")
def index():
    db = DB_Manager()

    all_books = db.load_entities(Book)
    # Hier wird später die Logik für den Warenkorb und die Produkte hinkommen
    return render_template("index.html", products=all_books)

if __name__ == "__main__":

    app.run(debug=True)