from flask import Blueprint, request, jsonify
from backend.services.attendance_service import AttendanceService

attendance_bp = Blueprint('attendance', __name__, url_prefix='/api')

@attendance_bp.route('/attendance/<reg_no>', methods=['GET'])
def get_attendance(reg_no):
    data = AttendanceService.get_student_attendance(reg_no.upper())
    return jsonify({
        "success": True,
        "reg_no": reg_no.upper(),
        **data
    })

@attendance_bp.route('/attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json() or {}
    reg_no = data.get('student_reg_no')
    subject_code = data.get('subject_code')
    faculty_id = data.get('faculty_id', 'FAC01')
    date = data.get('date')
    period = int(data.get('period', 1))
    status = data.get('status', 'Present')

    if not reg_no or not subject_code or not date:
        return jsonify({"success": False, "message": "Missing required attendance parameters."}), 400

    try:
        AttendanceService.mark_attendance(reg_no.upper(), subject_code, faculty_id, date, period, status)
        return jsonify({
            "success": True,
            "message": f"Attendance marked as '{status}' for {reg_no} in Period {period}."
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@attendance_bp.route('/attendance/batch', methods=['POST'])
def mark_batch_attendance():
    data = request.get_json() or {}
    faculty_id = data.get('faculty_id', 'FAC01')
    subject_code = data.get('subject_code')
    date = data.get('date')
    period = int(data.get('period', 1))
    attendance_list = data.get('attendance_list', [])

    if not subject_code or not date or not attendance_list:
        return jsonify({"success": False, "message": "Missing required batch attendance data."}), 400

    try:
        AttendanceService.mark_batch_attendance(faculty_id, subject_code, date, period, attendance_list)
        return jsonify({
            "success": True,
            "message": f"Successfully marked attendance for {len(attendance_list)} students for Period {period} on {date}."
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@attendance_bp.route('/reports/attendance', methods=['GET'])
def get_attendance_report():
    date = request.args.get('date', '2026-10-09')
    section = request.args.get('section', 'A').upper()
    report = AttendanceService.get_class_report(date, section)
    return jsonify({
        "success": True,
        "date": date,
        "section": section,
        "report": report
    })
