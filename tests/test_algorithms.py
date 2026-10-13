import unittest
import sys
import os

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.algorithms.searching import hash_table_search, binary_search, linear_search
from backend.algorithms.sorting import merge_sort_students
from backend.algorithms.graph_algorithms import bfs_campus_traversal, dijkstra_shortest_path, CAMPUS_GRAPH
from backend.algorithms.greedy import greedy_timetable_schedule
from backend.algorithms.backtracking import backtracking_timetable_schedule
from backend.algorithms.queues import FIFOQueue, PriorityQueueHeap
from backend.algorithms.dynamic_programming import optimize_study_plan_knapsack

class TestADSAlgorithms(unittest.TestCase):
    def setUp(self):
        self.sample_students = [
            {"reg_no": "25221A0503", "name": "Sai", "attendance_pct": 78.5},
            {"reg_no": "25221A0501", "name": "Aarav", "attendance_pct": 92.0},
            {"reg_no": "25221A0505", "name": "Sneha", "attendance_pct": 85.0},
            {"reg_no": "25221A0502", "name": "Harsha", "attendance_pct": 89.0}
        ]

    def test_algorithm_1_hash_table_search(self):
        students_dict = {s['reg_no']: s for s in self.sample_students}
        res = hash_table_search(students_dict, "25221A0501")
        self.assertTrue(res['found'])
        self.assertEqual(res['result']['name'], "Aarav")
        self.assertEqual(res['operations'], 1)

    def test_algorithm_2_binary_search(self):
        sorted_list = sorted(self.sample_students, key=lambda x: x['reg_no'])
        res = binary_search(sorted_list, "25221A0503")
        self.assertTrue(res['found'])
        self.assertEqual(res['result']['name'], "Sai")
        self.assertLessEqual(res['operations'], 3)

    def test_algorithm_6_merge_sort(self):
        res = merge_sort_students(self.sample_students, sort_key="reg_no")
        sorted_regs = [s['reg_no'] for s in res['sorted_data']]
        self.assertEqual(sorted_regs, ["25221A0501", "25221A0502", "25221A0503", "25221A0505"])

    def test_algorithm_3_graph_bfs_and_dijkstra(self):
        bfs_res = bfs_campus_traversal(start_node="MAIN_GATE")
        self.assertGreater(bfs_res['total_nodes_visited'], 5)

        dijk_res = dijkstra_shortest_path(start_node="MAIN_GATE", target_node="CSE_DEPT")
        self.assertEqual(dijk_res['path'][0], "MAIN_GATE")
        self.assertEqual(dijk_res['path'][-1], "CSE_DEPT")
        self.assertGreater(dijk_res['shortest_distance_meters'], 0)

    def test_algorithm_4_and_5_timetable_generation(self):
        subjects = [
            {"subject_code": "CS301", "subject_name": "ADS", "faculty_id": "FAC01", "periods_needed": 3},
            {"subject_code": "CS302", "subject_name": "Python", "faculty_id": "FAC02", "periods_needed": 3}
        ]
        faculties = ["FAC01", "FAC02"]
        rooms = ["LH-301", "LH-302"]

        greedy_res = greedy_timetable_schedule(subjects, faculties, rooms)
        self.assertEqual(greedy_res['assigned_periods'], 6)

        backtrack_res = backtracking_timetable_schedule(subjects, faculties, rooms)
        self.assertTrue(backtrack_res['success'])
        self.assertEqual(backtrack_res['scheduled_count'], 6)

    def test_algorithm_7_fifo_queue(self):
        q = FIFOQueue()
        q.enqueue("Task 1")
        q.enqueue("Task 2")
        self.assertEqual(q.dequeue(), "Task 1")
        self.assertEqual(q.dequeue(), "Task 2")

    def test_algorithm_8_priority_queue(self):
        pq = PriorityQueueHeap()
        pq.push("General Announcement", priority=1)
        pq.push("Urgent Exam Alert", priority=3)
        pq.push("Fee Reminder", priority=2)

        highest = pq.pop()
        self.assertEqual(highest['priority'], 3)
        self.assertEqual(highest['item'], "Urgent Exam Alert")

    def test_algorithm_9_dynamic_programming_knapsack(self):
        tasks = [
            {"task_name": "Module A", "hours": 2, "exam_weight": 20},
            {"task_name": "Module B", "hours": 3, "exam_weight": 30},
            {"task_name": "Module C", "hours": 4, "exam_weight": 40}
        ]
        res = optimize_study_plan_knapsack(tasks=tasks, total_available_hours=5)
        # Optimal: Module A (2h, 20) + Module B (3h, 30) = 5h, 50 weight
        self.assertEqual(res['max_score'], 50)
        self.assertEqual(res['total_hours_used'], 5)

if __name__ == '__main__':
    unittest.main()
