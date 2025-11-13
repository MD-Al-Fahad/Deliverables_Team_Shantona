import unittest
from main import app

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    def test_health(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()