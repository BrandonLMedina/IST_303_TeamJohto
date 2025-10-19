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
        
    cur = connection.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        about_me TEXT
    )
    ''')

    cur.execute('SELECT COUNT(*) FROM profile')
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("INSERT INTO profile (about_me) VALUES ('')")
        print("Inserted initial empty profile record.")

    cur.execute("INSERT INTO profile (about_me) VALUES (?)", ('',))

    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                ('First Post', 'Content for the first post')
                )

    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                ('Second Post', 'Content for the second post')
                )    

    connection.commit()
    connection.close()
    print("Database created and schema applied at instance/alumni_connect.db")

if __name__ == "__main__":
    init_db()
