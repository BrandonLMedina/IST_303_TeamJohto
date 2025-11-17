import sqlite3
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "instance" / "database.db"
SCHEMA_SQL = BASE_DIR / "schema.sql"

def reset_db():
    """Drop the existing DB file and recreate it from schema.sql."""

    # Remove old database if it exists
    if DB_PATH.exists():
        print(f"🗑 Removing old database at: {DB_PATH}")
        os.remove(DB_PATH)

    print("🆕 Creating new database from schema...")

    # Create a new empty DB file
    conn = sqlite3.connect(DB_PATH)

    # Enable foreign key enforcement
    conn.execute("PRAGMA foreign_keys = ON;")

    # Apply schema SQL
    with open(SCHEMA_SQL, "r", encoding="utf-8") as f:
        schema = f.read()
        conn.executescript(schema)

    conn.commit()
    conn.close()

    print(f"✅ Database reset complete — new tables created at {DB_PATH}")

# Run as script
if __name__ == "__main__":
    reset_db()
