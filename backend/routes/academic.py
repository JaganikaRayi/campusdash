from flask import Blueprint, request, jsonify
from database.db import get_db

academic_bp = Blueprint('academic', __name__, url_prefix='/api')

@academic_bp.route('/results/<reg_no>', methods=['GET'])
def get_results(reg_no):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, s.subject_name, s.credits
        FROM results r
        JOIN subjects s ON r.subject_code = s.subject_code
        WHERE r.student_reg_no = ?
        ORDER BY r.semester DESC, r.subject_code ASC
    """, (reg_no.upper(),))
    rows = [dict(r) for r in cursor.fetchall()]

    # Calculate SGPA / Total Credits
    total_credits = sum(r['credits'] for r in rows)
    weighted_points = sum(r['credits'] * r['grade_points'] for r in rows)
    sgpa = round(weighted_points / total_credits, 2) if total_credits > 0 else 0.0

    conn.close()
    return jsonify({
        "success": True,
        "reg_no": reg_no.upper(),
        "sgpa": sgpa,
        "total_credits": total_credits,
        "results": rows
    })

@academic_bp.route('/notifications', methods=['GET'])
def get_notifications():
    role = request.args.get('role', 'ALL').lower()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM notifications
        WHERE target_role = 'ALL' OR LOWER(target_role) = LOWER(?)
        ORDER BY priority DESC, posted_date DESC
    """, (role,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({
        "success": True,
        "notifications": rows
    })

@academic_bp.route('/notifications', methods=['POST'])
def add_notification():
    data = request.get_json() or {}
    title = data.get('title')
    message = data.get('message')
    category = data.get('category', 'Notice')
    priority = int(data.get('priority', 1))
    target_role = data.get('target_role', 'ALL')
    posted_date = data.get('posted_date', '2026-10-12')
    deadline = data.get('deadline')

    if not title or not message:
        return jsonify({"success": False, "message": "Title and message are required."}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notifications (title, message, category, priority, target_role, posted_date, deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, message, category, priority, target_role, posted_date, deadline))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Notification published successfully."}), 201

@academic_bp.route('/materials', methods=['GET'])
def get_materials():
    subject = request.args.get('subject')
    conn = get_db()
    cursor = conn.cursor()
    if subject:
        cursor.execute("""
            SELECT m.*, s.subject_name
            FROM study_materials m
            JOIN subjects s ON m.subject_code = s.subject_code
            WHERE m.subject_code = ?
            ORDER BY m.uploaded_at DESC
        """, (subject,))
    else:
        cursor.execute("""
            SELECT m.*, s.subject_name
            FROM study_materials m
            JOIN subjects s ON m.subject_code = s.subject_code
            ORDER BY m.uploaded_at DESC
        """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({
        "success": True,
        "materials": rows
    })

@academic_bp.route('/materials', methods=['POST'])
def add_material():
    data = request.get_json() or {}
    title = data.get('title')
    subject_code = data.get('subject_code')
    branch = data.get('branch', 'CSE')
    semester = int(data.get('semester', 3))
    file_url = data.get('file_url', 'https://campusdash.edu/materials/notes.pdf')
    description = data.get('description', '')
    uploaded_by = data.get('uploaded_by', 'Faculty')

    if not title or not subject_code:
        return jsonify({"success": False, "message": "Title and subject code are required."}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO study_materials (title, subject_code, branch, semester, file_url, description, uploaded_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, subject_code, branch, semester, file_url, description, uploaded_by))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Study material uploaded successfully."}), 201

@academic_bp.route('/faculty', methods=['GET'])
def get_faculty_directory():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faculty ORDER BY name ASC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({
        "success": True,
        "faculty": rows
    })

@academic_bp.route('/leave', methods=['GET'])
def get_leaves():
    reg_no = request.args.get('reg_no')
    conn = get_db()
    cursor = conn.cursor()
    if reg_no:
        cursor.execute("SELECT * FROM leave_applications WHERE student_reg_no = ? ORDER BY submitted_at DESC", (reg_no.upper(),))
    else:
        cursor.execute("SELECT * FROM leave_applications ORDER BY submitted_at DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({
        "success": True,
        "leaves": rows
    })

@academic_bp.route('/leave', methods=['POST'])
def submit_leave():
    data = request.get_json() or {}
    reg_no = data.get('student_reg_no')
    name = data.get('student_name', '')
    reason = data.get('reason')
    from_date = data.get('from_date')
    to_date = data.get('to_date')
    priority = int(data.get('priority', 1))

    if not reg_no or not reason or not from_date or not to_date:
        return jsonify({"success": False, "message": "All leave application fields are required."}), 400

    conn = get_db()
    cursor = conn.cursor()
    if not name:
        cursor.execute("SELECT name FROM students WHERE reg_no = ?", (reg_no.upper(),))
        s_row = cursor.fetchone()
        name = s_row['name'] if s_row else 'Student'

    cursor.execute("""
        INSERT INTO leave_applications (student_reg_no, student_name, reason, from_date, to_date, status, priority)
        VALUES (?, ?, ?, ?, ?, 'Pending', ?)
    """, (reg_no.upper(), name, reason, from_date, to_date, priority))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Leave application submitted successfully."}), 201

@academic_bp.route('/leave/<int:leave_id>', methods=['PUT'])
def update_leave_status(leave_id):
    data = request.get_json() or {}
    status = data.get('status', 'Approved')
    reviewed_by = data.get('reviewed_by', 'Administrator')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE leave_applications
        SET status = ?, reviewed_by = ?, reviewed_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (status, reviewed_by, leave_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": f"Leave application status updated to '{status}'."})

@academic_bp.route('/college-info', methods=['GET'])
def get_college_info():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM campus_locations")
    locs = [dict(l) for l in cursor.fetchall()]
    conn.close()

    return jsonify({
        "success": True,
        "college_name": "CampusDash Institute of Technology & Sciences (Autonomous)",
        "accreditation": "NAAC Grade 'A++', NBA Accredited CSE & ECE",
        "established": "1998",
        "departments": ["Computer Science & Engineering", "Data Science & AI", "Electronics & Communication", "Mechanical", "Civil"],
        "facilities": [
            "High Performance Computing & AI Research Lab",
            "Central Air-Conditioned Digital Library (50,000+ volumes)",
            "500-seat Acoustics Auditorium",
            "Indoor Sports Stadium & Olympic Gymnasium",
            "Automated Smart Campus IoT Sensors"
        ],
        "locations": locs
    })
