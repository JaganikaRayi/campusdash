-- CampusDash SQLite Schema
-- Automatically creates all tables for Campus Management System

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student', 'faculty', 'admin')),
    reg_no TEXT,
    name TEXT NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS students (
    reg_no TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    branch TEXT NOT NULL,
    section TEXT NOT NULL,
    academic_year INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    attendance_pct REAL DEFAULT 85.0
);

CREATE TABLE IF NOT EXISTS faculty (
    faculty_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    cabin TEXT,
    subjects TEXT
);

CREATE TABLE IF NOT EXISTS subjects (
    subject_code TEXT PRIMARY KEY,
    subject_name TEXT NOT NULL,
    branch TEXT NOT NULL,
    semester INTEGER NOT NULL,
    credits INTEGER NOT NULL,
    faculty_id TEXT,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_reg_no TEXT NOT NULL,
    subject_code TEXT NOT NULL,
    faculty_id TEXT,
    date TEXT NOT NULL,
    period INTEGER NOT NULL CHECK(period BETWEEN 1 AND 6),
    status TEXT NOT NULL CHECK(status IN ('Present', 'Absent', 'On Leave')),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_reg_no, subject_code, date, period),
    FOREIGN KEY (student_reg_no) REFERENCES students(reg_no),
    FOREIGN KEY (subject_code) REFERENCES subjects(subject_code)
);

CREATE TABLE IF NOT EXISTS fees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_reg_no TEXT UNIQUE NOT NULL,
    total_amount REAL NOT NULL,
    paid_amount REAL DEFAULT 0.0,
    balance_amount REAL NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_reg_no) REFERENCES students(reg_no)
);

CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_ref TEXT UNIQUE NOT NULL,
    student_reg_no TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_date TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('Successful', 'Pending', 'Failed')),
    receipt_no TEXT UNIQUE NOT NULL,
    FOREIGN KEY (student_reg_no) REFERENCES students(reg_no)
);

CREATE TABLE IF NOT EXISTS timetables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch TEXT NOT NULL,
    section TEXT NOT NULL,
    semester INTEGER NOT NULL,
    day_of_week TEXT NOT NULL,
    period INTEGER NOT NULL CHECK(period BETWEEN 1 AND 6),
    subject_code TEXT NOT NULL,
    faculty_id TEXT NOT NULL,
    room_no TEXT NOT NULL,
    start_time TEXT,
    end_time TEXT,
    FOREIGN KEY (subject_code) REFERENCES subjects(subject_code),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_reg_no TEXT NOT NULL,
    semester INTEGER NOT NULL,
    subject_code TEXT NOT NULL,
    internal_marks INTEGER NOT NULL,
    external_marks INTEGER NOT NULL,
    total_marks INTEGER NOT NULL,
    grade TEXT NOT NULL,
    grade_points INTEGER NOT NULL,
    UNIQUE(student_reg_no, semester, subject_code),
    FOREIGN KEY (student_reg_no) REFERENCES students(reg_no),
    FOREIGN KEY (subject_code) REFERENCES subjects(subject_code)
);

CREATE TABLE IF NOT EXISTS study_materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    subject_code TEXT NOT NULL,
    branch TEXT NOT NULL,
    semester INTEGER NOT NULL,
    file_url TEXT NOT NULL,
    description TEXT,
    uploaded_by TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_code) REFERENCES subjects(subject_code)
);

CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    category TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 1, -- 3: Urgent, 2: High, 1: Normal
    target_role TEXT DEFAULT 'ALL',
    posted_date TEXT NOT NULL,
    deadline TEXT
);

CREATE TABLE IF NOT EXISTS leave_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_reg_no TEXT NOT NULL,
    student_name TEXT NOT NULL,
    reason TEXT NOT NULL,
    from_date TEXT NOT NULL,
    to_date TEXT NOT NULL,
    status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'Approved', 'Rejected')),
    priority INTEGER DEFAULT 1, -- 3: Medical/Urgent, 2: Academic, 1: Personal
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_by TEXT,
    reviewed_at TIMESTAMP,
    FOREIGN KEY (student_reg_no) REFERENCES students(reg_no)
);

CREATE TABLE IF NOT EXISTS campus_locations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    building TEXT NOT NULL,
    floor TEXT,
    description TEXT
);
