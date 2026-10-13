import unittest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

class TestCampusDashAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['ads_algorithms_count'], 9)

    def test_student_list(self):
        response = self.client.get('/api/students')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertGreater(data['count'], 10)

    def test_algorithm_search_api(self):
        response = self.client.post('/api/algorithms/search', json={'target_reg_no': '25221A0501'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['hash_table']['found'])
        self.assertTrue(data['binary_search']['found'])

    def test_algorithm_knapsack_api(self):
        response = self.client.post('/api/algorithms/knapsack', json={'available_hours': 6})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertGreater(data['max_score'], 0)

if __name__ == '__main__':
    unittest.main()
