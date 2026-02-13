import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        message TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()



app.secret_key = "secret123"


# HOME PAGE
@app.route("/")
def index():   # 👈 IMPORTANT: endpoint name = index
    return render_template("index.html")


# ABOUT
@app.route("/about")
def about():
    return render_template("about.html")


# SERVICES
@app.route("/services")
def services():
    return render_template("services.html")


# GALLERY
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")




# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# ADMIN
@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM donations ORDER BY date DESC")
    donations = cursor.fetchall()

    conn.close()

    return render_template('admin.html', donations=donations)




# LOGOUT
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))


import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

#contact

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (name, email, phone, message) VALUES (?, ?, ?, ?)",
            (name, email, phone, message)
        )
        conn.commit()
        conn.close()

        return redirect("/contact")

    return render_template("contact.html")

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        amount = request.form['amount']
        payment_method = request.form['payment_method']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO donations (name, email, amount, payment_method)
            VALUES (?, ?, ?, ?)
        """, (name, email, amount, payment_method))

        conn.commit()
        conn.close()

        return redirect(url_for('donate'))

    return render_template('donate.html')




init_db()

if __name__ == "__main__":
    app.run(debug=True)
