from flask import Blueprint, request, jsonify
from backend.services.timetable_service import TimetableService
from database.db import get_db

timetable_bp = Blueprint('timetable', __name__, url_prefix='/api')

@timetable_bp.route('/timetable/<reg_no_or_section>', methods=['GET'])
def get_timetable(reg_no_or_section):
    target = reg_no_or_section.strip().upper()
    section = 'A'
    branch = 'CSE'

    # Check if target is a reg_no
    if len(target) > 5:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT section, branch FROM students WHERE reg_no = ?", (target,))
        s_row = cursor.fetchone()
        conn.close()
        if s_row:
            section = s_row['section']
            branch = s_row['branch']
    else:
        section = target

    rows = TimetableService.get_section_timetable(branch=branch, section=section)
    return jsonify({
        "success": True,
        "branch": branch,
        "section": section,
        "timetable": rows
    })

@timetable_bp.route('/timetable/faculty/<faculty_id>', methods=['GET'])
def get_faculty_timetable(faculty_id):
    rows = TimetableService.get_faculty_timetable(faculty_id.strip().upper())
    return jsonify({
        "success": True,
        "faculty_id": faculty_id.upper(),
        "timetable": rows
    })

@timetable_bp.route('/timetable/generate', methods=['POST'])
def generate_timetable():
    data = request.get_json() or {}
    algorithm = data.get('algorithm', 'backtracking')
    result = TimetableService.generate_ads_timetable(algorithm=algorithm)
    return jsonify({
        "success": True,
        "data": result
    })
