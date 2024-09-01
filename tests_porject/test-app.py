from flask import Flask, render_template
import sqlite3
app = Flask(__name__)


def create_db():
    with sqlite3.connect("flask_useres.db") as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS flask_useres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                join_date DATE NOT NULL

            )
        """
        )
        conn.commit()

def add_user():
    curser=

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    create_db()
    app.run(debug=True)
