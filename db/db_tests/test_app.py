from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "db_test_secret"

# --- Database connection helper ---
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), '../database/database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/add_alumni', methods=['GET', 'POST'])
def add_alumni():
    if request.method == 'POST':
        data = (
            request.form['first_name'],
            request.form['last_name'],
            request.form['email'],
            request.form['password_hash'],
            request.form['graduation_year']
        )
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO alumni (first_name, last_name, email, password_hash, graduation_year)
            VALUES (?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        flash("✅ Alumni added successfully!")
        return redirect(url_for('add_alumni'))
    return render_template('add_alumni.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        data = (
            request.form['first_name'],
            request.form['last_name'],
            request.form['email'],
            request.form['password_hash'],
            request.form['current_year'],
            request.form['expected_graduation_year']
        )
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO students (first_name, last_name, email, password_hash, current_year, expected_graduation_year)
            VALUES (?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        flash("✅ Student added successfully!")
        return redirect(url_for('add_student'))
    return render_template('add_student.html')

@app.route('/add_class', methods=['GET', 'POST'])
def add_class():
    if request.method == 'POST':
        data = (
            request.form['course_code'],
            request.form['class_name'],
            request.form['term'],
            request.form['year'],
            request.form['credits']
        )
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO classes (course_code, class_name, term, year, credits)
            VALUES (?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        flash("✅ Class added successfully!")
        return redirect(url_for('add_class'))
    return render_template('add_class.html')

@app.route('/view', methods=['GET'])
def view_table():
    # List of tables you can safely view
    tables = ['alumni', 'students', 'classes', 'industries', 'degree_concentrations', 'job_locations', 'user_classes']

    table = request.args.get('table')
    data = []

    if table and table in tables:
        conn = get_db_connection()
        try:
            data = conn.execute(f"SELECT * FROM {table}").fetchall()
        except sqlite3.Error as e:
            flash(f"Error fetching data: {e}")
        finally:
            conn.close()
    elif table and table not in tables:
        flash("Invalid table selected.")

    return render_template('view.html', tables=tables, table=table, data=data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # use different port from main app
