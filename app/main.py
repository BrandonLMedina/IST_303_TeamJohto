import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
import sqlite3

# --------------------------------------------------------------
# PATHS & CONFIG
# --------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')


app = Flask(
    __name__, 
     template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.config['SECRET_KEY'] = 'your secret key34165421654521'

# --------------------------------------------------------------
# DB CONNECTION
# --------------------------------------------------------------
def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --------------------------------------------------------------
# LOGIN PROTECTION
# --------------------------------------------------------------
@app.before_request
def require_login():
    allowed_routes = ['index', 'register', 'login', 'static']
    if request.endpoint not in allowed_routes and not session.get('logged_in'):
        return redirect(url_for('login'))


# --------------------------------------------------------------
# INDEX (HOMEPAGE)
# --------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# --------------------------------------------------------------
# LOGIN
# --------------------------------------------------------------
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

# --------------------------------------------------------------
# DASHBOARD (DYNAMIC)
# --------------------------------------------------------------
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user_type = session.get('user_type')
    user_id = session.get('user_id')

    conn = get_db_connection()
    cur = conn.cursor()

    # -------------------------
    # STUDENT QUERY
    # -------------------------
    if user_type == 'student':
        cur.execute("""
            SELECT
                s.student_id AS id,
                s.first_name,
                s.last_name,
                s.email,
                s.current_year,
                s.expected_graduation_year,
                s.is_seeking_mentorship,
                dc.degree_name,
                dc.concentration_name,
                ind.industry_name AS industry_name,
                jl.city,
                jl.state,
                jl.region
            FROM student s
            LEFT JOIN degree_concentrations dc
                ON s.degree_concentration_id = dc.degree_concentration_id
            LEFT JOIN industries ind
                ON s.desired_industry_id = ind.industry_id
            LEFT JOIN job_locations jl
                ON s.desired_job_location_id = jl.job_location_id
            WHERE s.student_id = ?
        """, (user_id,))

    # -------------------------
    # ALUMNI QUERY
    # -------------------------
    else:
        cur.execute("""
            SELECT
                a.alumni_id AS id,
                a.first_name,
                a.last_name,
                a.email,
                a.graduation_year,
                a.is_mentor,
                a.current_position,
                a.company_name,
                dc.degree_name,
                dc.concentration_name,
                ind.industry_name AS industry_name,
                jl.city,
                jl.state,
                jl.region
            FROM alumni a
            LEFT JOIN degree_concentrations dc
                ON a.degree_concentration_id = dc.degree_concentration_id
            LEFT JOIN industries ind
                ON a.industry_id = ind.industry_id
            LEFT JOIN job_locations jl
                ON a.job_location_id = jl.job_location_id
            WHERE a.alumni_id = ?
        """, (user_id,))

    row = cur.fetchone()
    conn.close()

    if row is None:
        flash('Could not load your profile. Please contact an administrator.')
        return redirect(url_for('logout'))

    row = dict(row)

    # LOCATION STRING BUILDER
    parts = []
    if row.get('city'):
        parts.append(row.get('city'))
    if row.get('state'):
        parts.append(row.get('state'))

    location_display = ', '.join(parts)
    region = row.get('region')
    if region:
        location_display = f"{location_display} ({region})" if location_display else region

    # FINAL DASHBOARD DATA
    dashboard = {
        'user_type': user_type,
        'full_name': f"{row.get('first_name', '')} {row.get('last_name', '')}".strip(),
        'id_label': 'Student ID' if user_type == 'student' else 'Alumni ID',
        'id_value': row.get('id'),
        'email': row.get('email'),
        'program': row.get('degree_name'),
        'concentration': row.get('concentration_name'),
        'location_display': location_display or None,
        'industry_name': row.get('industry_name'),

        # Student-specific
        'current_year': row.get('current_year') if user_type == 'student' else None,
        'expected_graduation_year': row.get('expected_graduation_year') if user_type == 'student' else None,
        'is_seeking_mentorship': bool(row.get('is_seeking_mentorship')) if user_type == 'student' else None,

        # Alumni-specific
        'graduation_year': row.get('graduation_year') if user_type == 'alumni' else None,
        'is_mentor': bool(row.get('is_mentor')) if user_type == 'alumni' else None,
        'company_name': row.get('company_name') if user_type == 'alumni' else None,
        'current_position': row.get('current_position') if user_type == 'alumni' else None,
    }

    return render_template('dashboard.html', dashboard=dashboard)

# --------------------------------------------------------------
# LOGOUT
# --------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out!')
    return redirect(url_for('login'))

# --------------------------------------------------------------
# PROFILE
# --------------------------------------------------------------    
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

# --------------------------------------------------------------
# CONTACTS
# --------------------------------------------------------------
user_contact = {}
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

# --------------------------------------------------------------
# REGISTER PAGE (UI ONLY for now)
# --------------------------------------------------------------
@app.route('/register')
def register():
    return render_template('register.html')

# --------------------------------------------------------------
# RUN APP
# --------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
