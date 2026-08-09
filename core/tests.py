from django.test import TestCase


class HealthEndpointTest(TestCase):
    def test_health_reports_application_and_database_readiness(self):
        response = self.client.get('/health/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok', 'database': 'ok'})

    def test_health_only_accepts_get_requests(self):
        response = self.client.post('/health/', {})

        self.assertEqual(response.status_code, 405)
