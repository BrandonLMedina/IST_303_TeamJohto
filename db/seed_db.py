import sqlite3
import csv
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent # /db
PROJECT_ROOT = BASE_DIR.parent  # project root
DB_PATH = BASE_DIR.parent / "instance" / "database.db" # /instance/database.db
DATA_DIR = BASE_DIR / "test_data" # /db/test_data

TABLES = {
    "degree_concentrations": DATA_DIR / "degree_concentrations.csv",
    "industries": DATA_DIR / "industries.csv",
    "job_locations": DATA_DIR / "job_locations.csv",
    "classes": DATA_DIR / "classes.csv",
    "alumni": DATA_DIR / "alumni.csv",
    "students": DATA_DIR / "students.csv",
    "user_classes": DATA_DIR / "user_classes.csv",
}

# Seed Table Function
def seed_table(cursor, table_name, csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        placeholders = ", ".join(["?"] * len(columns))
        column_list = ", ".join(columns)
        query = f"INSERT INTO {table_name} ({column_list}) VALUES ({placeholders})"
        for row in reader:
            cursor.execute(query, [row[col] for col in columns])

# Seed All Tables
def seed_all():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Maintain order due to foreign key dependencies
    ordered_tables = [
        "degree_concentrations",
        "industries",
        "job_locations",
        "classes",
        "alumni",
        "students",
        "user_classes",
    ]

    for table in ordered_tables:
        csv_path = TABLES.get(table)
        if not csv_path.exists():
            print(f"Skipping {table}: CSV not found at {csv_path}")
            continue
        seed_table(cur, table, csv_path)

    conn.commit()
    conn.close()
    print("✅ Database seeding complete.")

if __name__ == "__main__":
    seed_all()