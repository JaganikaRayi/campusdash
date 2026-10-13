from database.db import get_db

class AttendanceService:
    @staticmethod
    def mark_attendance(student_reg_no, subject_code, faculty_id, date, period, status):
        conn = get_db()
        cursor = conn.cursor()

        # Prevent duplicates
        cursor.execute("""
            SELECT id FROM attendance
            WHERE student_reg_no = ? AND subject_code = ? AND date = ? AND period = ?
        """, (student_reg_no, subject_code, date, period))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE attendance
                SET status = ?, faculty_id = ?, recorded_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, faculty_id, existing['id']))
        else:
            cursor.execute("""
                INSERT INTO attendance (student_reg_no, subject_code, faculty_id, date, period, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (student_reg_no, subject_code, faculty_id, date, period, status))

        conn.commit()
        # Recalculate percentage
        AttendanceService._update_student_attendance_pct(conn, student_reg_no)
        conn.close()
        return True

    @staticmethod
    def mark_batch_attendance(faculty_id, subject_code, date, period, attendance_list):
        """
        attendance_list: list of dicts: [{'reg_no': '...', 'status': 'Present'/'Absent'}]
        """
        conn = get_db()
        cursor = conn.cursor()

        for item in attendance_list:
            reg_no = item['reg_no']
            status = item['status']
            cursor.execute("""
                INSERT INTO attendance (student_reg_no, subject_code, faculty_id, date, period, status)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(student_reg_no, subject_code, date, period)
                DO UPDATE SET status = excluded.status, recorded_at = CURRENT_TIMESTAMP
            """, (reg_no, subject_code, faculty_id, date, period, status))

            AttendanceService._update_student_attendance_pct(conn, reg_no)

        conn.commit()
        conn.close()
        return True

    @staticmethod
    def _update_student_attendance_pct(conn, reg_no):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present
            FROM attendance
            WHERE student_reg_no = ?
        """, (reg_no,))
        row = cursor.fetchone()
        total = row['total'] or 0
        present = row['present'] or 0
        pct = round((present / total * 100), 1) if total > 0 else 85.0

        cursor.execute("UPDATE students SET attendance_pct = ? WHERE reg_no = ?", (pct, reg_no))
        conn.commit()

    @staticmethod
    def get_student_attendance(reg_no):
        conn = get_db()
        cursor = conn.cursor()

        # Overall summary
        cursor.execute("""
            SELECT COUNT(*) as total_periods,
                   SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present_periods,
                   SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) as absent_periods
            FROM attendance
            WHERE student_reg_no = ?
        """, (reg_no,))
        summary = dict(cursor.fetchone())
        total = summary['total_periods'] or 0
        present = summary['present_periods'] or 0
        summary['percentage'] = round((present / total * 100), 1) if total > 0 else 85.0

        # Subject-wise breakdown
        cursor.execute("""
            SELECT a.subject_code, s.subject_name,
                   COUNT(*) as total,
                   SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present,
                   SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) as absent
            FROM attendance a
            JOIN subjects s ON a.subject_code = s.subject_code
            WHERE a.student_reg_no = ?
            GROUP BY a.subject_code, s.subject_name
        """, (reg_no,))
        subject_wise = []
        for r in cursor.fetchall():
            item = dict(r)
            sub_total = item['total'] or 0
            sub_present = item['present'] or 0
            item['percentage'] = round((sub_present / sub_total * 100), 1) if sub_total > 0 else 0
            subject_wise.append(item)

        # Recent history logs
        cursor.execute("""
            SELECT a.id, a.date, a.period, a.status, a.subject_code, s.subject_name, f.name as faculty_name
            FROM attendance a
            JOIN subjects s ON a.subject_code = s.subject_code
            LEFT JOIN faculty f ON a.faculty_id = f.faculty_id
            WHERE a.student_reg_no = ?
            ORDER BY a.date DESC, a.period DESC
            LIMIT 30
        """, (reg_no,))
        history = [dict(r) for r in cursor.fetchall()]

        conn.close()
        return {
            "summary": summary,
            "subject_wise": subject_wise,
            "history": history
        }

    @staticmethod
    def get_class_report(date, section='A'):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.date, a.period, a.subject_code, s.subject_name,
                   COUNT(a.id) as total_marked,
                   SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_count,
                   SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) as absent_count
            FROM attendance a
            JOIN subjects s ON a.subject_code = s.subject_code
            JOIN students st ON a.student_reg_no = st.reg_no
            WHERE a.date = ? AND st.section = ?
            GROUP BY a.date, a.period, a.subject_code, s.subject_name
            ORDER BY a.period ASC
        """, (date, section))
        report = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return report
