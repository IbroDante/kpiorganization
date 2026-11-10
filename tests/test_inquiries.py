import unittest
from unittest.mock import patch

import requests
from app import app, BREVO_CONFIG


class InquiryTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.form = {
            'name': "Ada O'Brien",
            'email': 'ada@example.com',
            'phone': '+234123456789',
            'program': 'FinTech & Digital Assets',
            'message': '<script>alert(1)</script>',
        }
        self.config = patch.dict(BREVO_CONFIG, {
            'api_key': 'test-api-key',
            'sender_email': 'verified@example.com',
            'recipient_email': 'inbox@example.com',
        })
        self.config.start()
        self.addCleanup(self.config.stop)

    @patch('app.requests.post')
    def test_form_sends_original_brevo_payload_to_configured_inbox(self, post):
        post.return_value.status_code = 201
        response = self.client.post('/api/training-inquiry', json=self.form)
        self.assertEqual(response.status_code, 200)
        args, kwargs = post.call_args
        self.assertEqual(args[0], 'https://api.brevo.com/v3/smtp/email')
        self.assertEqual(kwargs['headers']['api-key'], 'test-api-key')
        payload = kwargs['json']
        self.assertEqual(payload['sender']['email'], 'verified@example.com')
        self.assertEqual(payload['to'][0]['email'], 'inbox@example.com')
        self.assertEqual(payload['replyTo']['email'], self.form['email'])
        self.assertIn("Ada O'Brien", payload['subject'])
        self.assertIn('FinTech &amp; Digital Assets', payload['htmlContent'])
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', payload['htmlContent'])
        self.assertIn('+234123456789', payload['htmlContent'])
        self.assertNotIn('<script>', payload['htmlContent'])

    @patch('app.requests.post')
    def test_brevo_rejection_and_network_failure_are_not_reported_as_success(self, post):
        post.return_value.status_code = 400
        self.assertEqual(self.client.post('/api/training-inquiry', json=self.form).status_code, 503)
        post.side_effect = requests.exceptions.Timeout()
        self.assertEqual(self.client.post('/api/training-inquiry', json=self.form).status_code, 503)

    @patch('app.requests.post')
    def test_missing_key_does_not_report_success(self, post):
        BREVO_CONFIG['api_key'] = ''
        self.assertEqual(self.client.post('/api/training-inquiry', json=self.form).status_code, 503)
        post.assert_not_called()

    @patch('app.requests.post')
    def test_invalid_inputs_do_not_reach_brevo(self, post):
        for data in ([], {}, {**self.form, 'email': 'invalid'},
                     {**self.form, 'name': 'Ada\nInjected'},
                     {**self.form, 'program': None}, {**self.form, 'message': 'x' * 10001}):
            with self.subTest(data=data):
                self.assertEqual(self.client.post('/api/training-inquiry', json=data).status_code, 400)
        post.assert_not_called()

    def test_unknown_api_route_is_not_html(self):
        response = self.client.get('/api/not-found')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.is_json)


if __name__ == '__main__':
    unittest.main()
