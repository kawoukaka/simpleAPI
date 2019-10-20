from unittest import TestCase, mock
from api_server import server
import json


class DeleteUserFromOrganizationTestCases(TestCase):
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

    def test_not_existed_user(self):
        server.user_tb = {
            'users': [{
                'user_first_name': 'John',
                'user_last_name': 'Doe',
                'user_email': 'John@att.com'
            }]
        }
        server.organization_tb = {'organizations': [{'org_name': 'CameraIQ'}]}
        server.user_org_tb = {
            'users': [
                {'user_email': 'John@att.com'}
            ],
            'organizations': [
                {'org_name': 'CameraIQ'}
            ]
        }
        response = self._post_rest_api('/v1/delete_user_from_organization', {
            'user_email': 'xxxx',
            'org_name': 'CameraIQ'
        })
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.json, {
            "message": "User does not exist!",
            "payload": {
                 'user_email': 'xxxx',
                 'org_name': 'CameraIQ'
            }
        })

    def test_not_existed_organization(self):
        server.user_tb = {
            'users': [{
                'user_first_name': 'John',
                'user_last_name': 'Doe',
                'user_email': 'John@att.com'
            }]
        }
        server.organization_tb = {'organizations': [{'org_name': 'CameraIQ'}]}
        server.user_org_tb = {
            'users': [
                {'user_email': 'John@att.com', 'organizations': ['CameraIQ']}
            ],
            'organizations': [
                {'org_name': 'CameraIQ', 'users': ['John']}
            ]
        }
        response = self._post_rest_api('/v1/delete_user_from_organization', {'user_email': 'John@att.com', 'org_name': 'xxxx'})
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.json, {
            "message": "Organization does not exist!",
            "payload": {
                'user_email': 'John@att.com',
                'org_name': 'xxxx'
            }
        })

    def test_database_schema_error(self):
        with mock.patch('api_server.server.user_org_tb', mock.MagicMock(side_effect={})):
            server.user_tb = {
                'users': [{
                    'user_first_name': 'John',
                    'user_last_name': 'Doe',
                    'user_email': 'John@att.com'
                }]
            }
            server.organization_tb = {'organizations': [{'org_name': 'CameraIQ'}]}
            response = self._post_rest_api('/v1/delete_user_from_organization', {
                'user_email': 'John@att.com',
                'org_name': 'CameraIQ'
            })
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json, {
                "message": "Database Schema Error!",
                "payload": {
                    'user_email': 'John@att.com',
                    'org_name': 'CameraIQ'
                }
            })

    def test_delete_user_from_organization_successfully(self):
        server.user_tb = {
            'users': [{
                'user_first_name': 'John',
                'user_last_name': 'Doe',
                'user_email': 'John@att.com'
            }]
        }
        server.organization_tb = {'organizations': [{'org_name': 'CameraIQ'}]}
        server.user_org_tb = {
            'users': [
                {'user_email': 'John@att.com', 'organizations': ['CameraIQ']}
            ],
            'organizations': [
                {'org_name': 'CameraIQ', 'users': ['John@att.com']}
            ]
        }
        response = self._post_rest_api('/v1/delete_user_from_organization', {
            'user_email': 'John@att.com',
            'org_name': 'CameraIQ'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "Deleted User from organization!",
            "payload": {
                'user_email': 'John@att.com',
                'org_name': 'CameraIQ'
            }
        })
