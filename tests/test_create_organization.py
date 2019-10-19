from unittest import TestCase, mock
from api_server import server
import json


@mock.patch('server.logger', mock.MagicMock())
class CreateOrganizationTestCases(TestCase):
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

    def test_already_existed_organization(self):
        server.organization_db = {'org_name': ['CameraIQ']}
        response = self._post_rest_api('/v1/create_organization', {'org_name': 'CameraIQ'})
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.json, {
            "message": "Organization name existed!",
            "payload": {
                "org_name": "CameraIQ"
            }
        })

    def test_create_organization_successfully(self):
        server.organization_db = {'org_name': []}
        response = self._post_rest_api('/v1/create_organization',  {'org_name': 'CameraIQ'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "Created Organization!",
            "payload": {'org_name': 'CameraIQ'}
        })
