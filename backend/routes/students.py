from flask import Blueprint, request, jsonify, session
from backend.services.student_service import StudentService

students_bp = Blueprint('students', __name__, url_prefix='/api')

@students_bp.route('/students', methods=['GET'])
def get_students():
    sort_by = request.args.get('sort_by', 'reg_no')
    reverse = request.args.get('reverse', 'false').lower() == 'true'
    search = request.args.get('search', '').strip().upper()
    section = request.args.get('section', '').strip().upper()

    students = StudentService.get_all_students(sort_by=sort_by, reverse=reverse)

    if section:
        students = [s for s in students if s.get('section') == section]

    if search:
        students = [s for s in students if search in s.get('reg_no', '') or search in s.get('name', '').upper()]

    return jsonify({
        "success": True,
        "count": len(students),
        "students": students
    })

@students_bp.route('/students/<reg_no>', methods=['GET'])
def get_student(reg_no):
    student = StudentService.get_student_by_reg_no(reg_no.upper())
    if not student:
        return jsonify({"success": False, "message": f"Student with registration number '{reg_no}' not found."}), 404

    return jsonify({
        "success": True,
        "student": student
    })

@students_bp.route('/students', methods=['POST'])
def create_student():
    data = request.get_json() or {}
    reg_no = data.get('reg_no')
    name = data.get('name')

    if not reg_no or not name:
        return jsonify({"success": False, "message": "Both 'reg_no' and 'name' are required fields."}), 400

    existing = StudentService.get_student_by_reg_no(reg_no.upper())
    if existing:
        return jsonify({"success": False, "message": f"Student with registration number '{reg_no}' already exists."}), 409

    try:
        new_student = StudentService.add_student(data)
        return jsonify({
            "success": True,
            "message": "Student created successfully.",
            "student": new_student
        }), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@students_bp.route('/students/<reg_no>', methods=['PUT'])
def update_student(reg_no):
    data = request.get_json() or {}
    student = StudentService.get_student_by_reg_no(reg_no.upper())
    if not student:
        return jsonify({"success": False, "message": f"Student '{reg_no}' not found."}), 404

    try:
        updated = StudentService.update_student(reg_no.upper(), data)
        return jsonify({
            "success": True,
            "message": "Student record updated successfully.",
            "student": updated
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@students_bp.route('/students/<reg_no>', methods=['DELETE'])
def delete_student(reg_no):
    student = StudentService.get_student_by_reg_no(reg_no.upper())
    if not student:
        return jsonify({"success": False, "message": f"Student '{reg_no}' not found."}), 404

    deleted = StudentService.delete_student(reg_no.upper())
    return jsonify({
        "success": True,
        "message": f"Student '{reg_no}' deleted successfully."
    })
