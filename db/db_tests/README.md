# Database Test Environment

This folder (`/db_tests`) contains a **lightweight Flask test application** used to verify that the main project’s SQLite database (`/instance/database.db`) and schema (`/database/schema.sql`) are functioning correctly.

These test forms are designed for quick data entry and inspection — **not for production use**.

---

## Folder Structure

```
/db_tests
│
├── test_app.py          # Standalone Flask app for database testing
├── templates/           # Minimal HTML form templates
│   ├── base.html
│   ├── add_alumni.html
│   ├── add_student.html
│   ├── view.html
│   └── add_class.html
└── README.md            # This file
```

---

## Purpose

- Validate that the SQLite schema and relationships work as expected.
- Test insert operations into tables such as `alumni`, `students`, and `classes`.
- Quickly verify database integrity without affecting the main Flask application.
- Provide a sandbox for development and debugging.

---

## Setup Instructions

### 1. Ensure your database exists

From the project root, initialize your database:

```bash
sqlite3 database/database.db < database/schema.sql
```

### 2. Run the test app

Navigate to this folder and run:

```bash
python test_app.py
```

By default, Flask will start on [http://127.0.0.1:5001](http://127.0.0.1:5001)

> Note: The port is set to **5001** to avoid conflicts with the main app (which typically uses 5000).

---

## Available Routes

| Route          | Description                                |
| -------------- | ------------------------------------------ |
| `/`            | Home page with navigation links            |
| `/add_alumni`  | Simple form to insert a new alumni record  |
| `/add_student` | Simple form to insert a new student record |
| `/add_class`   | Simple form to insert a new class record   |

Each page provides minimal input fields to test inserts into their corresponding database tables.

---

## Database Connection

The test app connects to:

```
../database/database.db
```

So the folder structure expects that the **database** folder exists one level above `/db_tests`.

So I have editted this line in `test_app.py`:

```python
db_path = os.path.join(os.path.dirname(__file__), 'instance/database.db')
```

---

## Data Verification

### Using SQLite CLI:

```bash
sqlite3 database/database.db
sqlite> SELECT * FROM alumni;
sqlite> SELECT * FROM students;
sqlite> SELECT * FROM classes;
```

---

## Notes & Warnings

- **This is a sandbox only.** It should not be deployed or merged into the production app.

---

**Created for internal testing**  
_Last updated: October 08, 2025_
