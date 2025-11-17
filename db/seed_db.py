import sqlite3
import csv
from pathlib import Path
from typing import List, Optional

# Paths
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DB_PATH = PROJECT_ROOT / "instance" / "database.db"
DATA_DIR = BASE_DIR / "test_data"

TABLES = {
    "degree_concentrations": DATA_DIR / "degree_concentrations.csv",
    "industries": DATA_DIR / "industries.csv",
    "job_locations": DATA_DIR / "job_locations.csv",
    "classes": DATA_DIR / "classes.csv",
    "users": DATA_DIR / "users.csv",
    "user_classes": DATA_DIR / "user_classes.csv",
}


def seed_table(cursor: sqlite3.Cursor, table_name: str, csv_path: Path) -> None:
    """Insert rows from a CSV file into a table, with trimming/cleaning."""
    
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # ─────────────────────────────────────────────
        # SAFETY CHECK: fieldnames can be None
        # ─────────────────────────────────────────────
        if reader.fieldnames is None:
            raise ValueError(f"CSV file {csv_path} has no header row!")

        if reader.fieldnames is None:
            raise ValueError(f"CSV file {csv_path} has no header row!")

        columns: List[str] = list(reader.fieldnames)

        placeholders = ", ".join("?" for _ in columns)
        column_list = ", ".join(columns)
        query = f"INSERT INTO {table_name} ({column_list}) VALUES ({placeholders})"

        for row in reader:
            cleaned_values: List[Optional[str]] = []

            for col in columns:
                val = row.get(col)

                # Normalize blank → NULL
                if val is None:
                    cleaned_values.append(None)
                    continue

                val = val.strip()
                if val == "":
                    cleaned_values.append(None)
                    continue

                # Clean Unicode
                val = val.replace("\u00A0", "").strip()  # non-breaking spaces

                # Fix profile_visibility
                if col == "profile_visibility":
                    v = val.lower().strip()

                    if v == "institution only":  # fix missing dash
                        v = "institution-only"

                    if v not in ("public", "private", "institution-only"):
                        raise ValueError(
                            f"Invalid profile_visibility '{val}' in CSV {csv_path}"
                        )

                    val = v

                cleaned_values.append(val)

            cursor.execute(query, cleaned_values)


def seed_all() -> None:
    """Seeds all tables in dependency order."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    ordered_tables = [
        "degree_concentrations",
        "industries",
        "job_locations",
        "classes",
        "users",
        "user_classes",
    ]

    for table in ordered_tables:
        csv_path = TABLES.get(table)

        # Pylance-safe null check
        if csv_path is None:
            print(f"⚠️ No CSV path defined for table: {table}")
            continue

        if not csv_path.exists():
            print(f"⚠️ Skipping {table}: CSV not found at {csv_path}")
            continue

        print(f"➡️ Seeding {table} ...")
        seed_table(cur, table, csv_path)

    conn.commit()
    conn.close()

    print("✅ Database seeding complete.")


if __name__ == "__main__":
    seed_all()
