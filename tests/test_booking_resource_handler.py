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


class BookingTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    @gen_test
    def test_booking_1(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchone = lambda: (1, 'Mr White')

        # Run operation
        url = self.get_url('/hotels/1/rooms/1/book')
        request = HTTPRequest(url=url, method='PUT', body=json_encode({'guest_name': 'Mr White'}))
        response = yield self.http_client.fetch(request)
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), {'room_id': 1, 'guest_name': 'Mr White'})

    @gen_test
    def test_booking_2(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchone = lambda: (1, 'Mr White')

        # Run operation
        url = self.get_url('/hotels/1/rooms/1/book')
        request = HTTPRequest(url=url, method='POST', body=json_encode({'guest_name': 'Mr White'}))
        response = yield self.http_client.fetch(request)
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), {'room_id': 1, 'guest_name': 'Mr White'})

    @gen_test
    def test_booking_3(self):
        self._app.db = Mock()
        url = self.get_url('/hotels/1/rooms/1/book')
        request = HTTPRequest(url=url, method='POST', body=json_encode({'guest': 'Mr White'}))
        try:
            response = yield self.http_client.fetch(request)
        except Exception as e:
            response = e
        self.assertEqual(response.code, 400)

    @gen_test
    def test_booking_4(self):
        self._app.db = Mock()
        url = self.get_url('/hotels/1/rooms/1/book')
        request = HTTPRequest(url=url, method='PUT', body=json_encode({}))
        try:
            response = yield self.http_client.fetch(request)
        except Exception as e:
            response = e
        self.assertEqual(response.code, 400)

    @gen_test
    def test_booking_5(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchone = lambda: (1, 'Mr White')

        # Run operation
        url = self.get_url('/hotels/1/rooms/1/book')
        request = HTTPRequest(url=url, method='DELETE')
        response = yield self.http_client.fetch(request)
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), {'room_id': 1, 'guest_name': 'Mr White'})
