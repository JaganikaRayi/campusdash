import sqlite3
import os
from werkzeug.security import generate_password_hash
from config import Config

def get_db():
    os.makedirs(os.path.dirname(Config.DATABASE), exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    with open(Config.SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    seed_db(conn)
    conn.close()

def generate_reg_numbers():
    # Supports 25221A0501 through 25221A0560 and hex suffixes A1..F4
    reg_nos = []
    # 01 through 60
    for i in range(1, 61):
        reg_nos.append(f"25221A05{i:02d}")
    # Hexadecimal style suffixes: A1..AF, B1..BF, C1..CF, D1..DF, E1..EF, F1..F4
    prefixes = ['A', 'B', 'C', 'D', 'E']
    for p in prefixes:
        for i in range(1, 10):
            reg_nos.append(f"25221A05{p}{i}")
    for i in range(1, 5):
        reg_nos.append(f"25221A05F{i}")
    return reg_nos

FIRST_NAMES = [
    "Aarav", "Ananya", "Sai", "Harsha", "Sneha", "Rahul", "Pooja", "Vikram",
    "Kavya", "Aditya", "Divya", "Rohit", "Varun", "Bhavana", "Kiran", "Meghana",
    "Pradeep", "Navya", "Ramesh", "Deepika", "Manoj", "Keerthi", "Suresh", "Sravani",
    "Gautam", "Swathi", "Akhil", "Tejaswi", "Karthik", "Sandhya", "Chaitanya", "Sireesha",
    "Naveen", "Vandana", "Mahesh", "Sushma", "Ganesh", "Madhuri", "Tarun", "Aparna"
]

LAST_NAMES = [
    "Reddy", "Sharma", "Rao", "Varma", "Goud", "Kumar", "Patel", "Chowdary",
    "Naidu", "Prasad", "Murthy", "Raju", "Gupta", "Mishra", "Joshi", "Babu"
]

def seed_db(conn):
    cursor = conn.cursor()
    # Check if already seeded
    cursor.execute("SELECT COUNT(*) as count FROM users")
    if cursor.fetchone()['count'] > 0:
        return

    # 1. Seed Admin
    cursor.execute("""
        INSERT INTO users (username, password_hash, role, name, email)
        VALUES (?, ?, ?, ?, ?)
    """, ('admin', generate_password_hash('admin123'), 'admin', 'College Administrator', 'admin@campusdash.edu'))

    # 2. Seed Faculty
    faculties = [
        ('FAC01', 'Dr. K. Srinivas Rao', 'CSE', 'srinivas.rao@campusdash.edu', '9848011221', 'Cabin 302, CS Block', 'CS301-ADS, CS302-Python'),
        ('FAC02', 'Prof. P. Radhika', 'CSE', 'radhika.p@campusdash.edu', '9848022332', 'Cabin 305, CS Block', 'CS303-Java Programming'),
        ('FAC03', 'Dr. M. Venkat', 'Mathematics', 'venkat.m@campusdash.edu', '9848033443', 'Cabin 108, Science Block', 'BS301-Discrete Mathematics'),
        ('FAC04', 'Prof. S. Anitha', 'ECE', 'anitha.s@campusdash.edu', '9848044554', 'Cabin 204, Tech Block', 'ES301-Engineering Science')
    ]
    for fac in faculties:
        cursor.execute("""
            INSERT INTO faculty (faculty_id, name, department, email, phone, cabin, subjects)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, fac)
        cursor.execute("""
            INSERT INTO users (username, password_hash, role, reg_no, name, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (fac[0], generate_password_hash('faculty123'), 'faculty', fac[0], fac[1], fac[3]))

    # 3. Seed Subjects
    subjects = [
        ('CS301', 'Advanced Data Structures & Algorithms', 'CSE', 3, 4, 'FAC01'),
        ('CS302', 'Python Programming Lab & Theory', 'CSE', 3, 3, 'FAC01'),
        ('CS303', 'Java Programming', 'CSE', 3, 3, 'FAC02'),
        ('BS301', 'Discrete Mathematics', 'CSE', 3, 4, 'FAC03'),
        ('ES301', 'Engineering Science Fundamentals', 'CSE', 3, 3, 'FAC04')
    ]
    for sub in subjects:
        cursor.execute("""
            INSERT INTO subjects (subject_code, subject_name, branch, semester, credits, faculty_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sub)

    # 4. Seed Students
    reg_numbers = generate_reg_numbers()
    branches = ['CSE']
    sections = ['A', 'B']

    for idx, reg_no in enumerate(reg_numbers):
        fn = FIRST_NAMES[idx % len(FIRST_NAMES)]
        ln = LAST_NAMES[(idx * 3) % len(LAST_NAMES)]
        name = f"{fn} {ln}"
        sec = sections[idx % len(sections)]
        email = f"{reg_no.lower()}@student.campusdash.edu"
        phone = f"98765{idx%90000+10000}"
        
        # Realistic attendance percentage between 72% and 98%
        att_pct = round(72.0 + ((idx * 7) % 27) + (idx % 3) * 0.5, 1)

        cursor.execute("""
            INSERT INTO students (reg_no, name, branch, section, academic_year, semester, email, phone, attendance_pct)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (reg_no, name, 'CSE', sec, 2, 3, email, phone, att_pct))

        # Add user account: Student logs in with reg_no and name/student123
        cursor.execute("""
            INSERT INTO users (username, password_hash, role, reg_no, name, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (reg_no, generate_password_hash('student123'), 'student', reg_no, name, email))

        # Seed Fees
        total_fee = 75000.0
        # Paid fee varied
        paid_options = [75000.0, 50000.0, 45000.0, 30000.0, 75000.0]
        paid = paid_options[idx % len(paid_options)]
        bal = total_fee - paid

        cursor.execute("""
            INSERT INTO fees (student_reg_no, total_amount, paid_amount, balance_amount)
            VALUES (?, ?, ?, ?)
        """, (reg_no, total_fee, paid, bal))

        # Seed Payments
        if paid > 0:
            cursor.execute("""
                INSERT INTO payments (transaction_ref, student_reg_no, amount, payment_date, payment_method, status, receipt_no)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (f"TXN-{reg_no}-01", reg_no, paid, '2026-08-15', 'UPI / NetBanking', 'Successful', f"REC-2026-{idx+1001}"))

        # Seed Results for 2nd Year Sem 1
        results_data = [
            (reg_no, 3, 'CS301', 28, 62, 90, 'A+', 10),
            (reg_no, 3, 'CS302', 26, 58, 84, 'A', 9),
            (reg_no, 3, 'CS303', 25, 54, 79, 'B+', 8),
            (reg_no, 3, 'BS301', 27, 60, 87, 'A', 9),
            (reg_no, 3, 'ES301', 29, 65, 94, 'O', 10)
        ]
        for r in results_data:
            cursor.execute("""
                INSERT INTO results (student_reg_no, semester, subject_code, internal_marks, external_marks, total_marks, grade, grade_points)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, r)

    # 5. Seed Attendance Records for key demonstration dates
    demo_dates = ['2026-10-05', '2026-10-06', '2026-10-07', '2026-10-08', '2026-10-09']
    schedule_blueprint = [
        (1, 'CS301', 'FAC01'),
        (2, 'CS302', 'FAC01'),
        (3, 'CS303', 'FAC02'),
        (4, 'BS301', 'FAC03'),
        (5, 'ES301', 'FAC04'),
        (6, 'CS301', 'FAC01')
    ]
    # Populate attendance for first 15 students for these dates
    for s_idx in range(15):
        s_reg = reg_numbers[s_idx]
        for d_idx, dt in enumerate(demo_dates):
            for period, sub, fac in schedule_blueprint:
                # 90% chance Present
                status = 'Present' if (s_idx + d_idx + period) % 11 != 0 else 'Absent'
                cursor.execute("""
                    INSERT OR IGNORE INTO attendance (student_reg_no, subject_code, faculty_id, date, period, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (s_reg, sub, fac, dt, period, status))

    # 6. Seed Timetable
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    tt_templates = [
        ('CS301', 'FAC01', 'LH-301', '09:00', '09:50'),
        ('CS302', 'FAC01', 'Lab-02', '09:50', '10:40'),
        ('CS303', 'FAC02', 'LH-301', '10:50', '11:40'),
        ('BS301', 'FAC03', 'LH-301', '11:40', '12:30'),
        ('ES301', 'FAC04', 'LH-302', '01:30', '02:20'),
        ('CS301', 'FAC01', 'LH-301', '02:20', '03:10')
    ]
    for d in days:
        for p_idx, slot in enumerate(tt_templates, start=1):
            cursor.execute("""
                INSERT INTO timetables (branch, section, semester, day_of_week, period, subject_code, faculty_id, room_no, start_time, end_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, ('CSE', 'A', 3, d, p_idx, slot[0], slot[1], slot[2], slot[3], slot[4]))

    # 7. Seed Notifications with Priorities (Urgent: 3, High: 2, Normal: 1)
    notifications = [
        ('Fee Due Deadline - Sem 3', 'All students must clear remaining tuition dues on or before Oct 25, 2026 to avoid exam hall ticket withholding.', 'Fee', 3, 'student', '2026-10-10', '2026-10-25'),
        ('Mid-Term Examination Schedule Announced', 'Mid-1 examinations for 2nd Year CSE will commence from November 2, 2026. Hall tickets available on portal.', 'Academic', 3, 'ALL', '2026-10-11', '2026-11-02'),
        ('Campus Placement Training - Python & ADS', 'Intensive placement training on Data Structures and Dynamic Programming starts this Saturday at Auditorium.', 'Placement', 2, 'student', '2026-10-08', '2026-10-20'),
        ('Faculty Meeting with Principal', 'HOD and faculty meeting scheduled in Boardroom at 3:30 PM regarding NAAC accreditation audit.', 'Administration', 2, 'faculty', '2026-10-11', '2026-10-12'),
        ('National Level Hackathon 2026', 'Registrations open for Smart Campus Innovation Hackathon. Cash prize of Rs 50,000 for winning team!', 'Event', 1, 'ALL', '2026-10-05', '2026-10-30')
    ]
    for notif in notifications:
        cursor.execute("""
            INSERT INTO notifications (title, message, category, priority, target_role, posted_date, deadline)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, notif)

    # 8. Seed Study Materials
    materials = [
        ('ADS Unit-1: Trees, Heaps and Balanced BSTs', 'CS301', 'CSE', 3, 'https://campusdash.edu/materials/ads-unit1.pdf', 'Complete lecture notes on AVL Trees and Binary Heaps', 'Dr. K. Srinivas Rao'),
        ('Python Advanced OOP & Generators Notes', 'CS302', 'CSE', 3, 'https://campusdash.edu/materials/python-adv.pdf', 'Hands-on examples of Python decorators, iterators and dunder methods', 'Dr. K. Srinivas Rao'),
        ('Java Collections Framework Master Guide', 'CS303', 'CSE', 3, 'https://campusdash.edu/materials/java-collections.pdf', 'ArrayList, HashMap and LinkedList performance trade-offs', 'Prof. P. Radhika'),
        ('Discrete Math: Recurrence Relations & Graphs', 'BS301', 'CSE', 3, 'https://campusdash.edu/materials/discrete-math.pdf', 'Step-by-step master theorem and graph theory proofs', 'Dr. M. Venkat')
    ]
    for mat in materials:
        cursor.execute("""
            INSERT INTO study_materials (title, subject_code, branch, semester, file_url, description, uploaded_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, mat)

    # 9. Seed Leave Applications (for FIFO queue & Priority Queue demonstration)
    leaves = [
        ('25221A0501', 'Aarav Reddy', 'Severe viral fever and doctor prescribed 3 days medical bed rest.', '2026-10-14', '2026-10-16', 'Pending', 3), # Medical/Urgent
        ('25221A0505', 'Sneha Goud', 'Sister wedding in hometown Hyderabad.', '2026-10-18', '2026-10-20', 'Pending', 1), # Personal
        ('25221A0512', 'Rohit Murthy', 'Representing college at Inter-University State Badminton Tournament.', '2026-10-15', '2026-10-17', 'Pending', 2), # Academic/Sports
        ('25221A0518', 'Navya Raju', 'Suffering from eye infection, unable to stare at monitors.', '2026-10-13', '2026-10-14', 'Approved', 3),
        ('25221A0522', 'Keerthi Babu', 'Family pilgrimage trip to Tirupati.', '2026-10-08', '2026-10-10', 'Approved', 1)
    ]
    for lv in leaves:
        cursor.execute("""
            INSERT INTO leave_applications (student_reg_no, student_name, reason, from_date, to_date, status, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, lv)

    # 10. Seed Campus Locations (for Graph BFS & Dijkstra algorithm demonstration)
    locations = [
        ('MAIN_GATE', 'Main Entrance Gate', 'Gate', 'Security Checkpoint', 'Ground Floor', 'Campus entrance gate and security desk'),
        ('ADMIN_BLOCK', 'Administrative Block', 'Office', 'Admin Building', '1st Floor', 'Principal office, Registrar and Accounts section'),
        ('CSE_DEPT', 'Computer Science Department', 'Academic', 'Tech Block A', '3rd Floor', 'CSE Lecture halls, AI lab and ADS coding labs'),
        ('LIBRARY', 'Central Digital Library', 'Facility', 'Knowledge Center', '2nd Floor', 'Reference books, digital journal access and silent study hall'),
        ('AUDITORIUM', 'APJ Abdul Kalam Auditorium', 'Event', 'Cultural Center', 'Ground Floor', '500-seat acoustic auditorium for seminars and events'),
        ('CAFETERIA', 'Campus Green Cafeteria', 'Dining', 'Student Activity Center', 'Ground Floor', 'Hygienic food court, snacks and refreshments'),
        ('SPORTS_COMPLEX', 'Indoor Sports Complex', 'Sports', 'Sports Pavilion', 'Ground Floor', 'Badminton, Table Tennis and Gymnasium'),
        ('HOSTEL_A', 'Boys Hostel Block A', 'Hostel', 'Residential Block', 'All Floors', 'Hostel accommodation and study rooms'),
        ('HOSTEL_B', 'Girls Hostel Block B', 'Hostel', 'Residential Block', 'All Floors', 'Hostel accommodation and study rooms')
    ]
    for loc in locations:
        cursor.execute("""
            INSERT INTO campus_locations (id, name, category, building, floor, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, loc)

    conn.commit()
