import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
import sqlite3


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')


app = Flask(
    __name__, 
     template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.config['SECRET_KEY'] = 'your secret key34165421654521'


def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


user_contact = {}
# Redirect users to login if not authenticated
@app.before_request
def require_login():
    allowed_routes = ['index', 'register', 'login', 'static']
    if request.endpoint not in allowed_routes and not session.get('logged_in'):
        return redirect(url_for('login'))


# Home route redirects to dashboard
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['username'].strip()
        password = request.form['password'].strip()

        conn = get_db_connection()
        cur = conn.cursor()

        # Find user in either Student or Alumni table
        cur.execute("""
            SELECT 'student' AS user_type, student_id AS id, first_name, email, password_hash 
            FROM student WHERE email = ?
            UNION ALL
            SELECT 'alumni' AS user_type, alumni_id AS id, first_name, email, password_hash 
            FROM alumni WHERE email = ?
        """, (email, email))
        user = cur.fetchone()
        conn.close()

        # Validate credentials
        if not user:
            error = 'Email not found. Please try again.'
        elif password != user['password_hash']:
            error = 'Invalid password. Please try again.'
        else:
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['user_type'] = user['user_type']
            session['email'] = user['email']
            flash(f"Welcome back, {user['first_name']}!")
            return redirect(url_for('dashboard'))

    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out!')
    return redirect(url_for('login'))
    
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get the first (and only) row from profile table
    cursor.execute('SELECT about_me FROM profile WHERE id = 1')
    row = cursor.fetchone()

    about_me = row['about_me'] if row else ''

    if request.method == 'POST':
        new_about = request.form.get('about_me', '')

        # Update existing record
        cursor.execute('UPDATE profile SET about_me = ? WHERE id = 1', (new_about,))
        conn.commit()
        conn.close()

        flash('Profile updated successfully!')
        return redirect(url_for('profile'))

    conn.close()
    return render_template('profile.html', about_me=about_me)


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    global user_contact
    if request.method == 'POST':
        phone = request.form.get('phone')
        email = request.form.get('email')
        linkedin = request.form.get('linkedin')
        github = request.form.get('github')

        # store the submitted info
        user_contact = {
            'phone': phone,
            'email': email,
            'linkedin': linkedin,
            'github': github
        }
        flash('Contact information saved successfully!')
        return redirect(url_for('contacts'))

    return render_template('contacts.html', contact_info=user_contact)    


@app.route('/register')
def register():
    return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True)
