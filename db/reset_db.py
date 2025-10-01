import sqlite3
from pathlib import Path
import seed_db

# Paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "instance" / "database.db"
SCHEMA_SQL = BASE_DIR / "schema.sql"

def reset_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Apply schema
    with open(SCHEMA_SQL, "r", encoding="utf-8") as f:
        schema = f.read()
        cur.executescript(schema)

    conn.commit()
    conn.close()
    print(f"✅ Database reset at {DB_PATH}")

    # Seed database
    seed_db.seed_from_csv()

if __name__ == "__main__":
    reset_db()