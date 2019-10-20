from unittest import TestCase, mock
from api_server import server
import json


class CreatUserTestCases(TestCase):
    def setUp(self):
        server.app.testing = True
        self.app = server.app.test_client()

    def tearDown(self):
        pass

    def _add_rest_headers(self, headers={}):
        headers['Content-Type'] = 'application/json'
        return headers

    def _post_rest_api(self, rest_url, payload):
        resp = self.app.post(
            rest_url,
            data=json.dumps(payload),
            headers=self._add_rest_headers()
        )
        return resp

    def test_already_existed_user(self):
        server.user_tb = {
            'users': [{
                'user_first_name': 'John',
                'user_last_name': 'Doe',
                'user_email': 'John@att.com'
            }]
        }
        response = self._post_rest_api('/v1/create_user', {
            'user_first_name': 'John',
            'user_last_name': 'Doe',
            'user_email': 'John@att.com'
        })
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.json, {
            "message": "User name existed!",
            "payload": {
                'user_first_name': 'John',
                'user_last_name': 'Doe',
                'user_email': 'John@att.com'
            }
        })

    def test_create_user_successfully(self):
        server.user_tb = {
            'users': []
        }
        response = self._post_rest_api('/v1/create_user',  {
            'user_first_name': 'John',
            'user_last_name': 'Doe',
            'user_email': 'John@att.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "Created User!",
            "payload": {
                'user_first_name': 'John',
                'user_last_name': 'Doe',
                'user_email': 'John@att.com'
            }
        })

