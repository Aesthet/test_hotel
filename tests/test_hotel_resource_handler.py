from tornado.testing import (
    AsyncHTTPTestCase,
    gen_test
)
from tornado.escape import (
    json_decode,
    json_encode
)
from tornado.httpclient import HTTPRequest
from mock import Mock

from app import make_app
from tests.common import mock_db_execute


class HotelTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    @gen_test
    def test_hotels_1(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchall = lambda: []

        # Run operation
        response = yield self.http_client.fetch(self.get_url('/hotels'))
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), [])

    @gen_test
    def test_hotels_2(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchall = lambda: [(1, 'santa')]

        # Run operation
        response = yield self.http_client.fetch(self.get_url('/hotels'))
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), [{'id': 1, 'name': 'santa'}])

    @gen_test
    def test_hotels_3(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchone = lambda: None

        # Run operation
        try:
            response = yield self.http_client.fetch(self.get_url('/hotels/1'))
        except Exception as e:
            response = e
        self.assertEqual(response.code, 404)

    @gen_test
    def test_hotels_4(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchone = lambda: (1, 'maria')

        # Run operation
        try:
            response = yield self.http_client.fetch(self.get_url('/hotels/1'))
        except Exception as e:
            response = e
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), {'id': 1, 'name': 'maria'})

    @gen_test
    def test_hotels_5(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchone = lambda: (1, 'new maria')

        # Run operation
        url = self.get_url('/hotels/1')
        request = HTTPRequest(url=url, method='PUT', body=json_encode({'name': 'new maria'}))
        response = yield self.http_client.fetch(request)
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), {'id': 1, 'name': 'new maria'})

    @gen_test
    def test_hotels_6(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchone = lambda: (1, 'maria')

        # Run operation
        url = self.get_url('/hotels')
        request = HTTPRequest(url=url, method='POST', body=json_encode({'name': 'maria'}))
        response = yield self.http_client.fetch(request)
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), {'id': 1, 'name': 'maria'})

    @gen_test
    def test_hotels_7(self):
        self._app.db = Mock()
        url = self.get_url('/hotels')
        request = HTTPRequest(url=url, method='POST', body=json_encode({'bad_key_name': 'maria'}))
        try:
            response = yield self.http_client.fetch(request)
        except Exception as e:
            response = e
        self.assertEqual(response.code, 400)

    @gen_test
    def test_hotels_8(self):
        self._app.db = Mock()
        url = self.get_url('/hotels/1')
        request = HTTPRequest(url=url, method='PUT', body=json_encode({'bad_key_name': 'maria'}))
        try:
            response = yield self.http_client.fetch(request)
        except Exception as e:
            response = e
        self.assertEqual(response.code, 400)

    @gen_test
    def test_hotels_9(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchone = lambda: (1, 'maria')

        # Run operation
        url = self.get_url('/hotels/1')
        request = HTTPRequest(url=url, method='DELETE')
        response = yield self.http_client.fetch(request)
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), {'id': 1, 'name': 'maria'})

