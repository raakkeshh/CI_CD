import unittest
from main import app

class CloudBuildProTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_dashboard_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CloudBuild Pro', response.data)

    def test_pipeline_route(self):
        response = self.client.get('/pipeline')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Manual Approval Gate', response.data)

    def test_history_route(self):
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Build History', response.data)

    def test_architecture_route(self):
        response = self.client.get('/architecture')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Architecture', response.data)

    def test_about_route(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Why Approval Gates', response.data)

    def test_health_api(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get('status'), 'HEALTHY')

    def test_pipeline_status_api(self):
        response = self.client.get('/api/pipeline/status')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('gate_status', data)

    def test_pipeline_approve_api(self):
        response = self.client.post('/api/pipeline/approve')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get('gate_status'), 'Approved')

    def test_pipeline_reject_api(self):
        response = self.client.post('/api/pipeline/reject')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get('gate_status'), 'Rejected')

if __name__ == '__main__':
    unittest.main()
