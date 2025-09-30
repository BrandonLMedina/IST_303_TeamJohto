-- schema.sql
DROP TABLE IF EXISTS alumni;
DROP TABLE IF EXISTS students;

CREATE TABLE alumni (
id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
graduation_year INTEGER NOT NULL,
degree TEXT NOT NULL,
major TEXT NOT NULL,
concentration TEXT,
email TEXT NOT NULL UNIQUE,
phone TEXT,
industry TEXT,
company TEXT,
position TEXT,
linkedin_url TEXT);

CREATE TABLE students (
id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
enrollment_year INTEGER NOT NULL,
expected_graduation_year INTEGER NOT NULL,
degree TEXT NOT NULL,
major TEXT NOT NULL,
concentration TEXT,
email TEXT NOT NULL UNIQUE,
phone TEXT,
linkedin_url TEXT);