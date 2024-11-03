import unittest
import json
from server import app

class TestServerIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_fetch_market_data_endpoint(self):
        # Test data
        test_payload = {
            'symbol': 'AAPL',
            'end_date': '2024-01-10'
        }

        # Make request to the endpoint
        response = self.app.post('/fetch_market_data',
                               data=json.dumps(test_payload),
                               content_type='application/json')
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check response structure
        self.assertIn('status', data)
        self.assertIn('data', data)
        self.assertEqual(data['status'], 'success')
        
        # Verify market data structure
        if data['data']:
            first_entry = data['data'][0]
            required_fields = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            for field in required_fields:
                self.assertIn(field, first_entry)

    def test_invalid_date_format(self):
        # Test with invalid date format
        test_payload = {
            'symbol': 'AAPL',
            'end_date': 'invalid-date'
        }

        response = self.app.post('/fetch_market_data',
                               data=json.dumps(test_payload),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('Invalid date format', data['error'])

if __name__ == '__main__':
    unittest.main() 