from database.db import get_db
from backend.algorithms.greedy import greedy_timetable_schedule
from backend.algorithms.backtracking import backtracking_timetable_schedule

class TimetableService:
    @staticmethod
    def get_section_timetable(branch='CSE', section='A', semester=3):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.day_of_week, t.period, t.subject_code, s.subject_name,
                   t.faculty_id, f.name as faculty_name, t.room_no, t.start_time, t.end_time
            FROM timetables t
            JOIN subjects s ON t.subject_code = s.subject_code
            JOIN faculty f ON t.faculty_id = f.faculty_id
            WHERE t.branch = ? AND t.section = ? AND t.semester = ?
            ORDER BY 
                CASE t.day_of_week 
                    WHEN 'Monday' THEN 1 
                    WHEN 'Tuesday' THEN 2 
                    WHEN 'Wednesday' THEN 3 
                    WHEN 'Thursday' THEN 4 
                    WHEN 'Friday' THEN 5 
                    WHEN 'Saturday' THEN 6 
                END, t.period ASC
        """, (branch, section, semester))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def get_faculty_timetable(faculty_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.day_of_week, t.period, t.subject_code, s.subject_name,
                   t.branch, t.section, t.room_no, t.start_time, t.end_time
            FROM timetables t
            JOIN subjects s ON t.subject_code = s.subject_code
            WHERE t.faculty_id = ?
            ORDER BY 
                CASE t.day_of_week 
                    WHEN 'Monday' THEN 1 
                    WHEN 'Tuesday' THEN 2 
                    WHEN 'Wednesday' THEN 3 
                    WHEN 'Thursday' THEN 4 
                    WHEN 'Friday' THEN 5 
                    WHEN 'Saturday' THEN 6 
                END, t.period ASC
        """, (faculty_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def generate_ads_timetable(algorithm="backtracking"):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.subject_code, s.subject_name, s.faculty_id, f.name as faculty_name
            FROM subjects s
            JOIN faculty f ON s.faculty_id = f.faculty_id
        """)
        raw_subjects = [dict(r) for r in cursor.fetchall()]
        conn.close()

        for s in raw_subjects:
            s['periods_needed'] = 6
            s['room_no'] = 'LH-301'

        rooms = ['LH-301', 'LH-302', 'Lab-01', 'Lab-02']
        faculties = ['FAC01', 'FAC02', 'FAC03', 'FAC04']

        if algorithm.lower() == "greedy":
            return greedy_timetable_schedule(raw_subjects, faculties, rooms)
        else:
            return backtracking_timetable_schedule(raw_subjects, faculties, rooms)
