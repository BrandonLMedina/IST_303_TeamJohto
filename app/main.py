import os
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
import sqlite3
import pandas as pd
from openai import OpenAI
import json
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()


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


client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# --------------------------------------------------------------
# DB CONNECTION
# --------------------------------------------------------------
def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
    
    
def get_industry_by_id(industry_id: int):
    industry_id = int(industry_id)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT industry_id, industry_name, sub_industry, description
        FROM industries
        WHERE industry_id = ?
    """, (industry_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return dict(row)


##openai search
@app.route("/api/job-opportunities", methods=["POST"])
def job_opportunities():
    # Require login
    if not session.get("logged_in"):
        return jsonify({"error": "User not logged in"}), 401

    user_id = session.get("user_id")
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json() or {}
    print("Incoming JSON:", data)

    # You *could* let frontend override, but simplest is to just ignore it:
    # industry_id_from_frontend = data.get("industry_id")
    # industry_name_from_frontend = data.get("industry_name")

    # Always use the user’s stored pathway
    industry_id = user.get("desired_industry_id") or user.get("industry_id")
    if not industry_id:
        return jsonify({"error": "User has no industry set"}), 400

    industry = get_industry_by_id(int(industry_id))
    if industry is None:
        return jsonify({"error": "industry not found"}), 404

    print("Industry found:", industry)

    industry_name_val = industry["industry_name"]
    sub_industry = industry["sub_industry"]
    description = industry["description"]

    prompt = f"""
You are a career advisor and job search assistant.

User profile:
- Name: {user['first_name']} {user['last_name']}
- User type: {user['user_type']}

Career pathway from database:
- Industry: {industry_name_val}
- Sub-industry: {sub_industry}
- Description: {description}

1. Propose 1–5 specific job titles that would be a strong match for THIS user.
2. For each, generate:
   - job_title
   - short_summary (1–2 sentences)
   -    - suggested_search_query (a short phrase we can paste into job sites, e.g. "entry level data analyst" or "software engineer internship")
   - recommended_keywords (comma-separated list)
   - typical_locations (short text, e.g. "Remote or major tech hubs")

Return ONLY a valid JSON list of objects, with no explanations, no markdown, and no code fences.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
    except Exception as e:
        print("OpenAI error:", repr(e))
        return jsonify({"error": f"OpenAI error: {str(e)}"}), 500

    content = (response.choices[0].message.content or "").strip()
    print("Raw OpenAI content:", content[:400], " ...")

    if content.startswith("```"):
        lines = content.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        content = "\n".join(lines).strip()

        # At this point, content *should* be pure JSON
    try:
        jobs = json.loads(content)
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return jsonify({
            "error": "AI response was not valid JSON",
            "raw": content
        }), 500

        # 🔗 Add search URLs for each job using the suggested_search_query
    for job in jobs:
        query = job.get("suggested_search_query") or job.get("job_title") or ""
        query_encoded = quote_plus(query)

        job["links"] = {
            "linkedin": f"https://www.linkedin.com/jobs/search/?keywords={query_encoded}",
            "indeed":   f"https://www.indeed.com/jobs?q={query_encoded}",
            # Add more if you want:
            # "glassdoor": f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query_encoded}",
        }

    return jsonify({"jobs": jobs}), 200


  

    

def get_user_by_id(user_id: int):
    """Fetch a user row as a dict."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            user_id,
            first_name,
            last_name,
            email,
            user_type,
            current_position,
            company_name,
            current_year,
            expected_graduation_year,
            graduation_year,
            desired_industry_id,
            industry_id
        FROM users
        WHERE user_id = ?
    """, (user_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return dict(row)


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
# LOGIN — unified users table
# --------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        email = request.form['username'].strip()
        password = request.form['password'].strip()

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT user_id, first_name, email, password_hash, user_type
            FROM users
            WHERE email = ?
        """, (email,))
        user = cur.fetchone()
        conn.close()

        if not user:
            error = "Email not found."
        elif password != user['password_hash']:  # (Later upgrade to hashing)
            error = "Invalid password."
        else:
            session['logged_in'] = True
            session['user_id'] = user['user_id']
            session['user_type'] = user['user_type']
            session['email'] = user['email']
            flash(f"Welcome back, {user['first_name']}!")
            return redirect(url_for('dashboard'))

    return render_template('login.html', error=error)


# --------------------------------------------------------------
# DASHBOARD (Unified — pulls student OR alumni fields dynamically)
# --------------------------------------------------------------
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_type = session['user_type']

    conn = get_db_connection()
    cur = conn.cursor()

    # IMPORTANT:
    # Students get desired_* lookups
    # Mentors get actual job_location_id & industry_id lookups
    cur.execute("""
        SELECT
            u.user_id AS id,
            u.user_type,
            u.first_name,
            u.last_name,
            u.email,
            u.phone_number,

            u.current_year,
            u.expected_graduation_year,
            u.graduation_year,
            u.current_position,
            u.company_name,

            u.profile_visibility,
            u.is_seeking_mentorship,
            u.is_mentor,

            dc.degree_level,
            dc.degree_name,
            dc.concentration_name,

            ind.industry_name,
            ind.sub_industry,
            ind.sector_code,
            ind.description AS industry_description,

            jl.organization_name AS loc_org,
            jl.city AS loc_city,
            jl.state AS loc_state,
            jl.country AS loc_country,
            jl.region AS loc_region

        FROM users u

        LEFT JOIN degree_concentrations dc
            ON u.degree_concentration_id = dc.degree_concentration_id

        LEFT JOIN industries ind
            ON ind.industry_id =
                CASE
                    WHEN u.user_type = 'student' THEN u.desired_industry_id
                    ELSE u.industry_id
                END

        LEFT JOIN job_locations jl
            ON jl.job_location_id =
                CASE
                    WHEN u.user_type = 'student' THEN u.desired_job_location_id
                    ELSE u.job_location_id
                END

        WHERE u.user_id = ?
    """, (user_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        flash("Could not load your dashboard.")
        return redirect(url_for('logout'))

    dashboard = dict(row)
    dashboard["full_name"] = f"{dashboard['first_name']} {dashboard['last_name']}"

    return render_template("dashboard.html", dashboard=dashboard)

# --------------------------------------------------------------
# PROFILE — Display + Edit (with dropdown lists)
# --------------------------------------------------------------
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_type = session['user_type']

    conn = get_db_connection()
    cur = conn.cursor()

    # MAIN unified SELECT
    cur.execute("""
        SELECT
            u.*,
            dc.degree_level,
            dc.degree_name,
            dc.concentration_name,

            ind.industry_name,
            ind.sub_industry,
            ind.sector_code,
            ind.description AS industry_description,

            jl.organization_name AS org_name,
            jl.city AS city,
            jl.state AS state,
            jl.country AS country,
            jl.region AS region

        FROM users u

        LEFT JOIN degree_concentrations dc
            ON u.degree_concentration_id = dc.degree_concentration_id

        LEFT JOIN industries ind
            ON ind.industry_id =
                CASE
                    WHEN u.user_type = 'student' THEN u.desired_industry_id
                    ELSE u.industry_id
                END

        LEFT JOIN job_locations jl
            ON jl.job_location_id =
                CASE
                    WHEN u.user_type = 'student' THEN u.desired_job_location_id
                    ELSE u.job_location_id
                END

        WHERE u.user_id = ?
    """, (user_id,))

    row = cur.fetchone()

    if not row:
        flash("Could not load your profile.")
        return redirect(url_for("dashboard"))

    profile = dict(row)

    # ----------------------------------------------------------
    # Fetch lists for dropdowns
    # ----------------------------------------------------------
    cur.execute("SELECT * FROM industries ORDER BY industry_name")
    industries = cur.fetchall()

    cur.execute("SELECT * FROM job_locations ORDER BY organization_name")
    locations = cur.fetchall()

    # ----------------------------------------------------------
    # SAVE CHANGES
    # ----------------------------------------------------------
    if request.method == "POST":

        updates = {
            "phone_number": request.form.get("phone_number"),
            "company_name": request.form.get("company_name"),
            "current_position": request.form.get("current_position"),
            "current_year": request.form.get("current_year"),
            "expected_graduation_year": request.form.get("expected_graduation_year"),
            "profile_visibility": request.form.get("profile_visibility"),
        }

        # Student vs Mentor fields
        if user_type == "student":
            updates["desired_job_location_id"] = request.form.get("job_location_id")
            updates["desired_industry_id"] = request.form.get("industry_id")
            updates["is_seeking_mentorship"] = request.form.get("is_seeking_mentorship")
        else:
            updates["job_location_id"] = request.form.get("job_location_id")
            updates["industry_id"] = request.form.get("industry_id")
            updates["is_mentor"] = request.form.get("is_mentor")

        # Build update query
        cols = ", ".join([f"{col} = ?" for col in updates])
        vals = list(updates.values()) + [user_id]

        cur.execute(f"UPDATE users SET {cols} WHERE user_id = ?", vals)
        conn.commit()
        conn.close()

        flash("Profile updated successfully!")
        return redirect(url_for("profile"))

    conn.close()
    return render_template(
        "profile.html",
        profile=profile,
        user_type=user_type,
        industries=industries,
        locations=locations
    )

# --------------------------------------------------------------
# REGISTER PAGE (UI ONLY for now)
# --------------------------------------------------------------
@app.route('/register')
def register():
    return render_template('register.html')

# --------------------------------------------------------------
# LOGOUT
# --------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out!')
    return redirect(url_for('login'))

# --------------------------------------------------------------
# RUN APP
# --------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
