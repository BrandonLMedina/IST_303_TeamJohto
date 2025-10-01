import sqlite3
import csv
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "instance" / "database.db"
ALUMNI_CSV = BASE_DIR / "alumni.csv"
STUDENTS_CSV = BASE_DIR / "students.csv"

def seed_from_csv():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Alumni
    with open(ALUMNI_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO alumni 
                (first_name, last_name, graduation_year, degree, major, concentration, email, phone, industry, company, position, linkedin_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["first_name"], row["last_name"], row["graduation_year"], row["degree"],
                row["major"], row["concentration"], row["email"], row["phone"],
                row["industry"], row["company"], row["position"], row["linkedin_url"]
            ))

    # Students
    with open(STUDENTS_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO students 
                (first_name, last_name, enrollment_year, expected_graduation_year, degree, major, concentration, email, phone, linkedin_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["first_name"], row["last_name"], row["enrollment_year"], row["expected_graduation_year"],
                row["degree"], row["major"], row["concentration"], row["email"], row["phone"], row["linkedin_url"]
            ))

    conn.commit()
    conn.close()
    print("✅ Database seeded with alumni & students")

if __name__ == "__main__":
    seed_from_csv()