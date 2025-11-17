-- ============================================================
-- CLEAN UNIFIED DATABASE SCHEMA (Students + Alumni Combined)
-- ============================================================

PRAGMA foreign_keys = OFF;

-- Drop tables in correct dependency order
DROP TABLE IF EXISTS user_classes;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS degree_concentrations;
DROP TABLE IF EXISTS industries;
DROP TABLE IF EXISTS job_locations;

PRAGMA foreign_keys = ON;

-- ============================================================
-- TABLE: degree_concentrations
-- Must be created BEFORE users references it
-- ============================================================

CREATE TABLE degree_concentrations (
    degree_concentration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    degree_name TEXT NOT NULL,
    concentration_name TEXT,
    department TEXT,
    description TEXT,
    degree_level TEXT 
        CHECK(degree_level IN ('Bachelors','Masters','PhD','Certificate','Professional Doctorate'))
        DEFAULT 'Masters',
    active BOOLEAN DEFAULT 1,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE: industries
-- ============================================================

CREATE TABLE industries (
    industry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    industry_name TEXT UNIQUE NOT NULL,
    sub_industry TEXT,
    description TEXT,
    sector_code TEXT,
    active BOOLEAN DEFAULT 1,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE: job_locations
-- ============================================================

CREATE TABLE job_locations (
    job_location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    state TEXT,
    country TEXT DEFAULT 'United States',
    region TEXT CHECK(region IN (
        'West Coast','East Coast','Midwest','South',
        'Europe','Asia-Pacific','Other'
    )),
    postal_code TEXT,
    organization_name TEXT,
    remote_option BOOLEAN DEFAULT 0,
    latitude REAL,
    longitude REAL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE: users
-- Unified table for both students and alumni
-- ============================================================

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_type TEXT CHECK (user_type IN ('student', 'alumni')) NOT NULL,

    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,

    phone_number TEXT,
    bio TEXT,
    resume_url TEXT,
    portfolio_url TEXT,
    linkedin_url TEXT,
    degree_concentration_id INTEGER,

    -- Student fields
    current_year INTEGER CHECK(current_year BETWEEN 1 AND 6),
    expected_graduation_year INTEGER,
    desired_industry_id INTEGER,
    desired_job_location_id INTEGER,
    is_seeking_mentorship BOOLEAN DEFAULT 0,

    -- Alumni fields
    graduation_year INTEGER,
    industry_id INTEGER,
    job_location_id INTEGER,
    current_position TEXT,
    company_name TEXT,
    is_mentor BOOLEAN DEFAULT 0,

    profile_visibility TEXT 
        CHECK(profile_visibility IN ('public','private','institution-only')) 
        DEFAULT 'institution-only',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (degree_concentration_id) REFERENCES degree_concentrations(degree_concentration_id)
        ON UPDATE CASCADE ON DELETE SET NULL,

    FOREIGN KEY (desired_industry_id) REFERENCES industries(industry_id)
        ON UPDATE CASCADE ON DELETE SET NULL,

    FOREIGN KEY (industry_id) REFERENCES industries(industry_id)
        ON UPDATE CASCADE ON DELETE SET NULL,

    FOREIGN KEY (desired_job_location_id) REFERENCES job_locations(job_location_id)
        ON UPDATE CASCADE ON DELETE SET NULL,

    FOREIGN KEY (job_location_id) REFERENCES job_locations(job_location_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

-- ============================================================
-- TABLE: classes
-- ============================================================

CREATE TABLE classes (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT UNIQUE NOT NULL,
    class_name TEXT NOT NULL,
    description TEXT,
    department TEXT,
    instructor_name TEXT,
    term TEXT CHECK(term IN ('Spring','Summer','Fall','Winter')),
    year INTEGER,
    credits REAL CHECK(credits >= 0),
    meeting_days TEXT,
    meeting_time TEXT,
    location TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE: user_classes
-- Links users → class enrollments
-- ============================================================

CREATE TABLE user_classes (
    user_class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,

    enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    completion_date DATETIME,
    grade TEXT CHECK(grade IN (
        'A','A-','B+','B','B-','C+','C','C-','D','F',
        'In Progress','Withdrawn'
    )),
    status TEXT CHECK(status IN ('enrolled','completed','dropped','auditing'))
        DEFAULT 'enrolled',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

