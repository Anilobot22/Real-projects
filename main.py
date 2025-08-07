from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import re

app = Flask(__name__)

# Create DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="115829955@Ak",
    database="univercity"
)
cursor = conn.cursor()

# Validate DB and Table names
def is_valid(name):
    return re.fullmatch(r"[A-Za-z0-9_]+", name) is not None

# Home/Login Page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        cursor.execute("SELECT * FROM univercity_login WHERE username=%s AND password=%s", (uname, pwd))
        user = cursor.fetchone()
        if user:
            return redirect(url_for('search'))
        else:
            return render_template('home.html', msg="Invalid credentials")
    return render_template('home.html')

# Search Page
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        db_name = request.form['database']
        table_name = request.form['tablename']

        if not is_valid(db_name) or not is_valid(table_name):
            return "Invalid database or table name!"

        try:
            cursor.execute(f"USE `{db_name}`")
        except Exception as e:
            return f"Error switching database: {e}"

        return redirect(url_for('view_table', database=db_name, tablename=table_name))

    return render_template('search.html')

# View Table Page
@app.route('/view/<database>/<tablename>')
def view_table(database, tablename):
    if not is_valid(database) or not is_valid(tablename):
        return "Invalid input!"

    try:
        cursor.execute(f"USE `{database}`")
        cursor.execute(f"SELECT * FROM `{tablename}`")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return render_template('view.html', table=tablename, columns=columns, data=rows)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
