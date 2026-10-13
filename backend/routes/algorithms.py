from flask import Blueprint, request, jsonify
from backend.services.student_service import StudentService
from backend.algorithms.searching import hash_table_search, binary_search, linear_search
from backend.algorithms.sorting import merge_sort_students
from backend.algorithms.graph_algorithms import bfs_campus_traversal, dijkstra_shortest_path, CAMPUS_GRAPH, LOCATION_LABELS
from backend.algorithms.greedy import greedy_timetable_schedule
from backend.algorithms.backtracking import backtracking_timetable_schedule
from backend.algorithms.queues import compare_queue_order
from backend.algorithms.dynamic_programming import optimize_study_plan_knapsack
from database.db import get_db

algorithms_bp = Blueprint('algorithms', __name__, url_prefix='/api/algorithms')

@algorithms_bp.route('/search', methods=['POST'])
def run_search_benchmark():
    data = request.get_json() or {}
    target_reg_no = data.get('target_reg_no', '25221A0515').strip().upper()

    benchmark = StudentService.search_benchmark(target_reg_no)
    return jsonify({
        "success": True,
        **benchmark
    })

@algorithms_bp.route('/sort', methods=['POST'])
def run_sort():
    data = request.get_json() or {}
    key = data.get('sort_key', 'attendance_pct')
    reverse = bool(data.get('reverse', True))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT reg_no, name, branch, section, attendance_pct FROM students")
    records = [dict(r) for r in cursor.fetchall()]
    conn.close()

    result = merge_sort_students(records, sort_key=key, reverse=reverse)
    return jsonify({
        "success": True,
        **result
    })

@algorithms_bp.route('/graph', methods=['POST'])
def run_graph():
    data = request.get_json() or {}
    algorithm = data.get('algorithm', 'dijkstra').lower()
    start_node = data.get('start_node', 'MAIN_GATE')
    target_node = data.get('target_node', 'CSE_DEPT')

    if algorithm == 'bfs':
        result = bfs_campus_traversal(start_node=start_node)
    else:
        result = dijkstra_shortest_path(start_node=start_node, target_node=target_node)

    return jsonify({
        "success": True,
        "available_nodes": LOCATION_LABELS,
        **result
    })

@algorithms_bp.route('/timetable', methods=['POST'])
def run_timetable():
    data = request.get_json() or {}
    algorithm = data.get('algorithm', 'backtracking').lower()

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

    if algorithm == 'greedy':
        result = greedy_timetable_schedule(raw_subjects, faculties, rooms)
    else:
        result = backtracking_timetable_schedule(raw_subjects, faculties, rooms)

    return jsonify({
        "success": True,
        **result
    })

@algorithms_bp.route('/queues', methods=['POST'])
def run_queues():
    data = request.get_json() or {}
    custom_items = data.get('items')

    if not custom_items:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, student_reg_no, student_name, reason, priority, submitted_at FROM leave_applications")
        custom_items = [dict(r) for r in cursor.fetchall()]
        conn.close()

    result = compare_queue_order(custom_items)
    return jsonify({
        "success": True,
        **result
    })

@algorithms_bp.route('/knapsack', methods=['POST'])
def run_knapsack():
    data = request.get_json() or {}
    hours = data.get('available_hours', 8)
    tasks = data.get('tasks')

    result = optimize_study_plan_knapsack(tasks=tasks, total_available_hours=hours)
    return jsonify({
        "success": True,
        **result
    })
