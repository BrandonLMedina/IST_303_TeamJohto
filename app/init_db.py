# app/init_db.py
import sqlite3
from pathlib import Path

def init_db():
    # Ensure instance folder exists
    Path("instance").mkdir(exist_ok=True)

    # Create/connect to DB
    connection = sqlite3.connect("instance/database.db")

    # Run schema.sql
    with open("db/schema.sql", "r") as f:
        connection.executescript(f.read())

    connection.commit()
    connection.close()
    print("Database created and schema applied at instance/alumni_connect.db")

if __name__ == "__main__":
    init_db()
