-- ============================================================
-- DATABASE SCHEMA: Alumni & Student Information System
-- ============================================================

-- Drop tables in dependency order (junctions first)
DROP TABLE IF EXISTS user_classes;
DROP TABLE IF EXISTS alumni;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS degree_concentrations;
DROP TABLE IF EXISTS industries;
DROP TABLE IF EXISTS job_locations;

-- ============================================================
-- TABLE: alumni
-- Stores information about graduates, including professional data
-- ============================================================

CREATE TABLE alumni (
    alumni_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,                  -- Hashed password for secure login
    graduation_year INTEGER,
    degree_concentration_id INTEGER,
    industry_id INTEGER,
    job_location_id INTEGER,
    current_position TEXT,                        -- e.g., "Data Engineer"
    company_name TEXT,                            -- e.g., "Google"
    linkedin_url TEXT,
    resume_url TEXT,
    portfolio_url TEXT,
    bio TEXT,                                     -- Short professional summary
    phone_number TEXT,
    is_mentor BOOLEAN DEFAULT 0,                  -- Indicates willingness to mentor students
    profile_visibility TEXT 
        CHECK(profile_visibility IN ('public', 'private', 'institution-only')) 
        DEFAULT 'public',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (degree_concentration_id) REFERENCES degree_concentrations(degree_concentration_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (industry_id) REFERENCES industries(industry_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (job_location_id) REFERENCES job_locations(job_location_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

-- ============================================================
-- TABLE: students
-- Stores information about current students, career interests, and mentorship needs
-- ============================================================

CREATE TABLE student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,                   -- Hashed password for secure login
    current_year INTEGER CHECK(current_year BETWEEN 1 AND 6), -- Year in program
    expected_graduation_year INTEGER,
    degree_concentration_id INTEGER,
    desired_industry_id INTEGER,
    desired_job_location_id INTEGER,
    resume_url TEXT,
    portfolio_url TEXT,
    bio TEXT,
    phone_number TEXT,
    is_seeking_mentorship BOOLEAN DEFAULT 0,
    profile_visibility TEXT 
        CHECK(profile_visibility IN ('public', 'private', 'institution-only')) 
        DEFAULT 'institution-only',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (degree_concentration_id) REFERENCES degree_concentrations(degree_concentration_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (desired_industry_id) REFERENCES industries(industry_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (desired_job_location_id) REFERENCES job_locations(job_location_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

-- ============================================================
-- TABLE: user_classes
-- Shared junction table linking both students and alumni to classes
-- ============================================================

CREATE TABLE user_classes (
    user_class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_type TEXT NOT NULL 
        CHECK(user_type IN ('student', 'alumni')),    -- Type of user
    user_id INTEGER NOT NULL,                         -- FK reference depends on user_type
    class_id INTEGER NOT NULL,
    enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    completion_date DATETIME,
    grade TEXT CHECK(grade IN ('A','A-','B+','B','B-','C+','C','C-','D','F','In Progress','Withdrawn')),
    status TEXT 
        CHECK(status IN ('enrolled', 'completed', 'dropped', 'auditing')) 
        DEFAULT 'enrolled',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (class_id) REFERENCES classes(class_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- ============================================================
-- TABLE: classes
-- Stores course and scheduling information
-- ============================================================

CREATE TABLE classes (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT UNIQUE NOT NULL,                -- e.g., "ISTM-602"
    class_name TEXT NOT NULL,                        -- e.g., "Data Management and Analytics"
    description TEXT,
    department TEXT,                                 -- e.g., "Information Systems & Technology"
    instructor_name TEXT,                            -- Could later become FK to faculty table
    term TEXT CHECK(term IN ('Spring', 'Summer', 'Fall', 'Winter')), 
    year INTEGER,
    credits REAL CHECK(credits >= 0),                -- e.g., 3.0
    meeting_days TEXT,                               -- e.g., "Mon/Wed"
    meeting_time TEXT,                               -- e.g., "6:00 PM - 8:50 PM"
    location TEXT,                                   -- e.g., "Burkle 14" or "Online"
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE: degree_concentrations
-- Reference table for academic degree and concentration programs
-- ============================================================

CREATE TABLE degree_concentrations (
    degree_concentration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    degree_name TEXT NOT NULL,                       -- e.g., "M.S. in Information Systems & Technology"
    concentration_name TEXT,                         -- e.g., "Data Science and Analytics"
    department TEXT,                                 -- e.g., "Center for IS&T"
    description TEXT,
    degree_level TEXT 
    CHECK(degree_level IN ('Bachelors', 'Masters', 'PhD', 'Certificate', 'Professional Doctorate')) 
    DEFAULT 'Masters',
    active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE: industries
-- Reference table for employment sectors and sub-industries
-- ============================================================

CREATE TABLE industries (
    industry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    industry_name TEXT UNIQUE NOT NULL,               -- e.g., "Information Technology"
    sub_industry TEXT,                                -- e.g., "Cybersecurity"
    description TEXT,
    sector_code TEXT,                                 -- Optional: NAICS or internal code
    active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE: job_locations
-- Reference table for employment and desired job locations
-- ============================================================

CREATE TABLE job_locations (
    job_location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    state TEXT,
    country TEXT DEFAULT 'United States',
    region TEXT CHECK(region IN ('West Coast', 'East Coast', 'Midwest', 'South', 'Europe', 'Asia-Pacific', 'Other')),
    postal_code TEXT,
    organization_name TEXT,                           -- e.g., "Google Mountain View"
    remote_option BOOLEAN DEFAULT 0,                  -- 1 = supports remote/hybrid work
    latitude REAL,
    longitude REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);