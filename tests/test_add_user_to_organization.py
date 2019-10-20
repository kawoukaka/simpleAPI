from unittest import TestCase, mock
from api_server import server
import json


class AddUserToOrganizationTestCases(TestCase):
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

    def test_non_existed_user(self):
        response = self._post_rest_api('/v1/add_user_to_organization', {'user_email': 'xx', 'org_name': 'CameraIQ'})
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.json, {
            "message": "User does not exist!",
            "payload": {
                "user_email": "xx",
                "org_name": "CameraIQ"
            }
        })

    def test_non_existed_organization(self):
        server.user_tb = {
            'users': [{
                'user_first_name': 'John',
                'user_last_name': 'Doe',
                'user_email': 'John@att.com'
            }]
        }
        response = self._post_rest_api('/v1/add_user_to_organization', {
            'user_email': 'John@att.com',
            'org_name': 'xxxx'
        })
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.json, {
            "message": "Organization does not exist!",
            "payload": {
                "user_email": "John@att.com",
                "org_name": "xxxx"
            }
        })

    def test_add_user_to_organization_successfully(self):
        server.user_tb = {
            'users': [{
                'user_first_name': 'John',
                'user_last_name': 'Doe',
                'user_email': 'John@att.com'
            }]
        }
        server.organization_tb = {'organizations': [{'org_name': 'CameraIQ'}]}
        response = self._post_rest_api('/v1/add_user_to_organization', {
            'user_email': 'John@att.com',
            'org_name': 'CameraIQ'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "Added User in Organization!",
            "payload": {
                'user_email': 'John@att.com',
                'org_name': 'CameraIQ'
            }
        })
