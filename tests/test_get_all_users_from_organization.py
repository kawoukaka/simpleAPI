from unittest import TestCase, mock
from api_server import server
import json


@mock.patch('server.logger', mock.MagicMock())
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

    def test_not_existed_organization(self):
        server.user_db = {'user_name': ['John']}
        server.organization_db = {'org_name': ['CameraIQ']}
        server.user_org_db = {
            'users': [
                {'user_name': 'John'}
            ],
            'organizations': [
                {'org_name': 'CameraIQ'}
            ]
        }
        response = self._post_rest_api('/v1/get_users_from_organization', {'org_name': 'xxxx'})
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.json, {
            "message": "Organization does not exist!",
            "payload": {
                'org_name': 'xxxx'
            }
        })

    def test_database_schema_error(self):
        with mock.patch('api_server.server.user_org_db', mock.MagicMock(side_effect={})):
            server.user_db = {'user_name': ['John']}
            server.organization_db = {'org_name': ['CameraIQ']}
            response = self._post_rest_api('/v1/get_users_from_organization', {'user_name': 'John', 'org_name': 'CameraIQ'})
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json, {
                "message": "Database Schema Error!",
                "payload": {
                    'user_name': 'John',
                    'org_name': 'CameraIQ'
                }
            })

    def test_get_users_from_organization_successfully(self):
        server.user_db = {'user_name': ['John']}
        server.organization_db = {'org_name': ['CameraIQ']}
        server.user_org_db = {
            'users': [
                {'user_name': 'John', 'organizations': ['CameraIQ']}
            ],
            'organizations': [
                {'org_name': 'CameraIQ', 'users': ['John']}
            ]
        }
        response = self._post_rest_api('/v1/get_users_from_organization', {'org_name': 'CameraIQ'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "results": ['John'],
            "payload": {
                'org_name': 'CameraIQ'
            }
        })
