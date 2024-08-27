import sqlite3
from io import BytesIO

import pandas as pd
from flask import Flask, jsonify, redirect, render_template, request, send_file
from loguru import logger
from openpyxl.styles import Font
from openpyxl.styles.alignment import Alignment


app = Flask(__name__)


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


@app.route("/")
def index():
    return render_template("index.html")


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
    return redirect("/")




@app.route("/download")
def download():
    # Fetch data from the database
    with sqlite3.connect("people.db") as conn:
        df = pd.read_sql_query(
            "SELECT name, phone, number_guests, side, relationship FROM people", conn
        )
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
        sheet.append([f" {total_guests} :מספר המוזמנים "])
        last_row = sheet.max_row
        for cell in sheet[last_row]:
            cell.alignment = Alignment(horizontal="center")
            cell.font = Font(size=14)

        # Set column width to fit the content and align to center
        for column in sheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                # Center align the content
                cell.alignment = Alignment(horizontal="center")

                # Calculate the maximum length of the content in the column
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass

            # Adjust the width of the column based on the maximum content length
            adjusted_width = max_length + 2
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
    return redirect("/")


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


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
