import sqlite3
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "instance" / "database.db"
SCHEMA_SQL = BASE_DIR / "schema.sql"

# Reset Function
def reset_db():
    # Remove old database if it exists
    if DB_PATH.exists():
        print(f"Removing old database at {DB_PATH}")
        os.remove(DB_PATH)

    # Recreate an empty database file
    print("Creating new database from schema...")
    conn = sqlite3.connect(DB_PATH)

    # Apply schema
    with open(SCHEMA_SQL, "r", encoding="utf-8") as f:
        schema = f.read()
        conn.executescript(schema)

    conn.commit()
    conn.close()

    print(f"Database reset complete — new blank tables created at {DB_PATH}")

# Run as script
if __name__ == "__main__":
    reset_db()
