from database.db import get_db
from werkzeug.security import generate_password_hash
from backend.algorithms.searching import hash_table_search, binary_search, linear_search
from backend.algorithms.sorting import merge_sort_students

class StudentService:
    @staticmethod
    def get_all_students(sort_by="reg_no", reverse=False):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()

        # Use ADS Merge Sort
        sorted_result = merge_sort_students(rows, sort_key=sort_by, reverse=reverse)
        return sorted_result['sorted_data']

    @staticmethod
    def get_student_by_reg_no(reg_no):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE reg_no = ?", (reg_no,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def add_student(data):
        conn = get_db()
        cursor = conn.cursor()
        reg_no = data.get('reg_no').strip().upper()
        name = data.get('name').strip()
        branch = data.get('branch', 'CSE')
        section = data.get('section', 'A')
        academic_year = int(data.get('academic_year', 2))
        semester = int(data.get('semester', 3))
        email = data.get('email', f"{reg_no.lower()}@student.campusdash.edu")
        phone = data.get('phone', '9876543210')
        att_pct = float(data.get('attendance_pct', 85.0))

        cursor.execute("""
            INSERT INTO students (reg_no, name, branch, section, academic_year, semester, email, phone, attendance_pct)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (reg_no, name, branch, section, academic_year, semester, email, phone, att_pct))

        # Create user login
        cursor.execute("""
            INSERT INTO users (username, password_hash, role, reg_no, name, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (reg_no, generate_password_hash('student123'), 'student', reg_no, name, email))

        # Initialize fee record
        total_fee = 75000.0
        cursor.execute("""
            INSERT INTO fees (student_reg_no, total_amount, paid_amount, balance_amount)
            VALUES (?, ?, ?, ?)
        """, (reg_no, total_fee, 0.0, total_fee))

        conn.commit()
        conn.close()
        return StudentService.get_student_by_reg_no(reg_no)

    @staticmethod
    def update_student(reg_no, data):
        conn = get_db()
        cursor = conn.cursor()
        name = data.get('name')
        branch = data.get('branch')
        section = data.get('section')
        email = data.get('email')
        phone = data.get('phone')

        cursor.execute("""
            UPDATE students
            SET name = COALESCE(?, name),
                branch = COALESCE(?, branch),
                section = COALESCE(?, section),
                email = COALESCE(?, email),
                phone = COALESCE(?, phone)
            WHERE reg_no = ?
        """, (name, branch, section, email, phone, reg_no))

        cursor.execute("""
            UPDATE users
            SET name = COALESCE(?, name),
                email = COALESCE(?, email)
            WHERE reg_no = ?
        """, (name, email, reg_no))

        conn.commit()
        conn.close()
        return StudentService.get_student_by_reg_no(reg_no)

    @staticmethod
    def delete_student(reg_no):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM attendance WHERE student_reg_no = ?", (reg_no,))
        cursor.execute("DELETE FROM payments WHERE student_reg_no = ?", (reg_no,))
        cursor.execute("DELETE FROM fees WHERE student_reg_no = ?", (reg_no,))
        cursor.execute("DELETE FROM results WHERE student_reg_no = ?", (reg_no,))
        cursor.execute("DELETE FROM leave_applications WHERE student_reg_no = ?", (reg_no,))
        cursor.execute("DELETE FROM users WHERE reg_no = ?", (reg_no,))
        cursor.execute("DELETE FROM students WHERE reg_no = ?", (reg_no,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted

    @staticmethod
    def search_benchmark(target_reg_no):
        """
        Executes Linear, Binary, and Hash Search on current dataset to benchmark ADS algorithms
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()

        # Dictionary for Hash Table O(1)
        students_dict = {s['reg_no']: s for s in rows}
        hash_res = hash_table_search(students_dict, target_reg_no)

        # Sorted list for Binary Search O(log n)
        sorted_students = sorted(rows, key=lambda x: x['reg_no'])
        binary_res = binary_search(sorted_students, target_reg_no)

        # Raw list for Linear Search O(n)
        linear_res = linear_search(rows, target_reg_no)

        return {
            "target": target_reg_no,
            "total_records": len(rows),
            "hash_table": hash_res,
            "binary_search": binary_res,
            "linear_search": linear_res
        }
