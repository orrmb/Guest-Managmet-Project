import sqlite3
from io import BytesIO
import pandas as pd
from flask import Flask, jsonify, redirect, render_template, request, send_file, session, url_for
from loguru import logger
from openpyxl.styles import Font
from openpyxl.styles.alignment import Alignment



app = Flask(__name__)

app.config['SECRET_KEY'] = '12-!897321kjh'

# Database setup
def init_db():
    with sqlite3.connect("people.db") as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                number_guests INTEGER NOT NULL,
                side TEXT NOT NULL,
                relationship TEXT NOT NULL
            )
        """
        )
        conn.commit()

with sqlite3.connect("flask_useres.db") as conn:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS flask_useres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            join_date DATE

        )
    """
    )
    conn.commit()

with sqlite3.connect("expenses.db") as conn:
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                owner TEXT NOT NULL,
                amount REAL NOT NULL,
                phone TEXT NOT NULL,
                payment_date TEXT,
                comments TEXT

        )
    """
    )
    conn.commit()

@app.route("/")
def login_page():
    return render_template("login-page.html")

@app.route("/addguest", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/wedding_expenses")
def wedding_expenses():
    return render_template("wedding-expenses.html")

@app.route("/arranging_tables")
def arranging_tables():
    return render_template("arranging-tables.html")

@app.route("/home", methods=["GET"])
def home_page():
    return render_template("home-page.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    passd = request.form["password"]
    with sqlite3.connect("flask_useres.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT username, password from flask_useres where username = '{username}' ")
        user = cursor.fetchone()
        cursor.close()
        if user and passd == user[1]:
            session['username']  = user[0]
            return redirect(url_for('home_page'))
        else:
            return render_template('login-page.html', error='שם משתמש או סיסמא אינם נכונים, נסה שנית או שתפנה למנהל .מערכת.')

            
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    phone = request.form["phone"]
    number_guests = request.form["number"]
    side = request.form["side"]
    relationship = request.form["relationship"]
    with sqlite3.connect("people.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO people (name, phone, number_guests, side, relationship) VALUES (?, ?, ?, ?, ?)", 
            (name, phone, number_guests, side, relationship),
        )
        conn.commit()
    return redirect("/addguest")


@app.route("/download")
def download():
    # Fetch data from the database
    with sqlite3.connect("people.db") as conn:
        df = pd.read_sql_query(
            "SELECT name, phone, number_guests, side, relationship FROM people", conn
        )

    # Convert DataFrame to Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="People")
        sheet = writer.sheets["People"]
        
        # Add the total number of guests in the last row
        total_guests = get_total_guests()
        sheet.append([f"Total Guests: {total_guests}"])
        last_row = sheet.max_row
        for cell in sheet[last_row]:
            cell.alignment = Alignment(horizontal="center")
            cell.font = Font(size=14)

        # Set column width to fit the content and align to center
        for column in sheet.columns:
            max_length = max(len(str(cell.value)) for cell in column if cell.value)
            adjusted_width = max_length + 2
            sheet.column_dimensions[column[0].column_letter].width = adjusted_width

        # Make the sheet RTL
        sheet.sheet_view.rightToLeft = True

    output.seek(0)

    # Serve the file as a downloadable attachment
    return send_file(
        output,
        as_attachment=True,
        download_name="people.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@app.route("/clear", methods=["POST"])
def clear():
    with sqlite3.connect("people.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE people")
        conn.commit()
        init_db()
    return redirect("/addguest")


def get_total_guests():
    with sqlite3.connect("people.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM people")
        myresulet = cursor.fetchall()
        total_guests = sum(row[3] for row in myresulet)
        conn.commit()
        return total_guests


@app.route("/guest_table", methods=["GET"])
def guest_table():
    with sqlite3.connect("people.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM people")
        myresulet = cursor.fetchall()

        total_guests = get_total_guests()

    if not myresulet:
        logger.info("The table is empty")
        return render_template("empty-table.html")
    else:
        logger.info("Displaying the table in route /guest_table")
        return render_template(
            "guest_table.html", rows=myresulet, totalguests=total_guests
        )

    
@app.route("/delete", methods=["POST"])
def delete_guest():
    guest_id = request.form["id"]
    with sqlite3.connect("people.db") as conn:
        conn.execute("DELETE FROM people WHERE id = ?", (guest_id,))
        conn.commit()
        total_guests = get_total_guests()
        total_guests = get_total_guests()
    return jsonify({"totalguests": total_guests})


@app.route("/edit", methods=["POST"])
def edit_guest():
    guest_id = request.form["id"]
    name_edit = request.form["name"]
    phone_edit = request.form["phone"]
    number_guests_edit = request.form["number"]
    side_edit = request.form["side"]
    relationship_edit = request.form["relationship"]

    with sqlite3.connect("people.db") as conn:
        conn.execute(
            """
            UPDATE people
            SET name = ?, phone = ?, number_guests = ?, side = ?, relationship = ?
            WHERE id = ?
            
        """, 
            (

                name_edit, 
                phone_edit, 
                number_guests_edit, 
                side_edit, 
                relationship_edit, 
                guest_id,
            ),
        )
        conn.commit()
        total_guests = get_total_guests()
        total_guests = get_total_guests()
    return jsonify({"totalguests": total_guests})

@app.route("/save_expense", methods=["POST"])
def save_expense():
    data = request.json
    expense_id = data.get("id")
    name = data.get("name")
    owner = data.get("owner")
    amount = data.get("amount")
    phone = data.get("phone")
    payment_date = data.get("payment_date")
    comments = data.get("comments")

    with sqlite3.connect("expenses.db") as conn:
        cursor = conn.cursor()
        if expense_id:
            cursor.execute(
                """
                UPDATE expenses
                SET name = ?, owner = ?, amount = ?, phone = ?, payment_date = ?, comments = ?
                WHERE id = ?
                """,
                (name, owner, amount, phone, payment_date, comments, expense_id)
            )
        else:
            cursor.execute(
                """
                INSERT INTO expenses (name, owner, amount, phone, payment_date, comments)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, owner, amount, phone, payment_date, comments)
            )
        conn.commit()
    return jsonify({"success": True})

@app.route("/get_expenses")
def get_expenses():
    with sqlite3.connect("expenses.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
    return jsonify([
        {
            "id": row[0],
            "name": row[1],
            "owner": row[2],
            "amount": row[3],
            "phone": row[4],
            "payment_date": row[5],
            "comments": row[6]
        }
        for row in expenses
    ])

@app.route("/get_expense/<int:id>")
def get_expense(id):
    with sqlite3.connect("expenses.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (id,))
        expense = cursor.fetchone()
    if expense:
        return jsonify({
            "id": expense[0],
            "name": expense[1],
            "owner": expense[2],
            "amount": expense[3],
            "phone": expense[4],
            "payment_date": expense[5],
            "comments": expense[6]
        })
    else:
        return jsonify({}), 404

@app.route("/delete_expense/<int:id>", methods=["DELETE"])
def delete_expense(id):
    with sqlite3.connect("expenses.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
        conn.commit()
    return jsonify({"success": True})




if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)
