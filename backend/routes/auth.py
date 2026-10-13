from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from database.db import get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', 'student').lower().strip()

    if not username:
        return jsonify({"success": False, "message": "Username or Registration Number is required."}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Look up in users table
    cursor.execute("SELECT * FROM users WHERE (UPPER(username) = UPPER(?) OR UPPER(reg_no) = UPPER(?))", (username, username))
    user = cursor.fetchone()

    # Check if student is logging in with registration number and name (as per prompt req 3)
    if not user and role == 'student':
        cursor.execute("SELECT * FROM students WHERE UPPER(reg_no) = UPPER(?)", (username,))
        student = cursor.fetchone()
        if student and password.strip().lower() == student['name'].strip().lower():
            # Matched name as password!
            cursor.execute("SELECT * FROM users WHERE UPPER(reg_no) = UPPER(?)", (username,))
            user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"success": False, "message": "Invalid username or registration number."}), 401

    user_dict = dict(user)

    # Validate role
    if user_dict['role'] != role and role != 'any':
        conn.close()
        return jsonify({"success": False, "message": f"User is registered as {user_dict['role']}, not {role}."}), 403

    # Validate password if user has password
    # For students, allow either correct password hash OR their registered student name
    is_valid_pwd = False
    if password:
        if check_password_hash(user_dict['password_hash'], password):
            is_valid_pwd = True
        elif user_dict['role'] == 'student':
            # Check against student name (case-insensitive)
            cursor.execute("SELECT name FROM students WHERE reg_no = ?", (user_dict.get('reg_no'),))
            s_row = cursor.fetchone()
            if s_row and password.strip().lower() in s_row['name'].strip().lower():
                is_valid_pwd = True

    if not is_valid_pwd:
        conn.close()
        return jsonify({"success": False, "message": "Incorrect password or name credentials."}), 401

    # Fetch extra profile details
    profile = {}
    if user_dict['role'] == 'student':
        cursor.execute("SELECT * FROM students WHERE reg_no = ?", (user_dict.get('reg_no'),))
        s_row = cursor.fetchone()
        if s_row:
            profile = dict(s_row)
    elif user_dict['role'] == 'faculty':
        cursor.execute("SELECT * FROM faculty WHERE faculty_id = ?", (user_dict.get('reg_no'),))
        f_row = cursor.fetchone()
        if f_row:
            profile = dict(f_row)

    conn.close()

    # Set server-side session
    session['user_id'] = user_dict['id']
    session['username'] = user_dict['username']
    session['role'] = user_dict['role']
    session['reg_no'] = user_dict.get('reg_no')
    session['name'] = user_dict['name']

    return jsonify({
        "success": True,
        "message": f"Welcome back, {user_dict['name']}!",
        "user": {
            "id": user_dict['id'],
            "username": user_dict['username'],
            "role": user_dict['role'],
            "reg_no": user_dict.get('reg_no'),
            "name": user_dict['name'],
            "email": user_dict['email'],
            "profile": profile
        }
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Successfully logged out."})

@auth_bp.route('/auth/current', methods=['GET'])
def get_current_user():
    if 'user_id' not in session:
        return jsonify({"authenticated": False}), 200

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, reg_no, name, email FROM users WHERE id = ?", (session['user_id'],))
    user = cursor.fetchone()
    conn.close()

    if not user:
        session.clear()
        return jsonify({"authenticated": False}), 200

    return jsonify({
        "authenticated": True,
        "user": dict(user)
    })
