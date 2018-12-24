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


class RoomTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    @gen_test
    def test_rooms_1(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchall = lambda: []

        # Run operation
        response = yield self.http_client.fetch(self.get_url('/hotels/1/rooms'))
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), [])

    @gen_test
    def test_rooms_2(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchall = lambda: [(1, 11, 1, 1, 'Mr White'), (2, 21, 1, 2, None)]

        # Run operation
        response = yield self.http_client.fetch(self.get_url('/hotels/1/rooms'))
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body),
                         [{'id': 1, 'room_number': 11, 'hotel_id': 1, 'floor_number': 1, 'guest_name': 'Mr White'},
                          {'id': 2, 'room_number': 21, 'hotel_id': 1, 'floor_number': 2, 'guest_name': None}])

    @gen_test
    def test_rooms_3(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchone = lambda: None

        # Run operation
        try:
            response = yield self.http_client.fetch(self.get_url('/hotels/1/rooms/1'))
        except Exception as e:
            response = e
        self.assertEqual(response.code, 404)

    @gen_test
    def test_rooms_4(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchone = lambda: (1, 11, 1, 1)

        # Run operation
        try:
            response = yield self.http_client.fetch(self.get_url('/hotels/1/rooms/1'))
        except Exception as e:
            response = e
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), {'id': 1, 'room_number': 11, 'hotel_id': 1, 'floor_number': 1})

    @gen_test
    def test_rooms_5(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchone = lambda: (1, 31, 1, 3)

        # Run operation
        url = self.get_url('/hotels/1/rooms/1')
        request = HTTPRequest(url=url, method='PUT', body=json_encode({'room_number': 3, 'floor_number': 3}))
        response = yield self.http_client.fetch(request)
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), {'id': 1, 'room_number': 31, 'hotel_id': 1, 'floor_number': 3})

    @gen_test
    def test_rooms_6(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchone = lambda: (3, 41, 1, 4)

        # Run operation
        url = self.get_url('/hotels/1/rooms')
        request = HTTPRequest(url=url, method='POST', body=json_encode({'room_number': 41, 'floor_number': 4}))
        response = yield self.http_client.fetch(request)
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), {'id': 3, 'room_number': 41, 'hotel_id': 1, 'floor_number': 4})

    @gen_test
    def test_rooms_7(self):
        self._app.db = Mock()
        url = self.get_url('/hotels/1/rooms')
        request = HTTPRequest(url=url, method='POST', body=json_encode({'room_number': 42}))
        try:
            response = yield self.http_client.fetch(request)
        except Exception as e:
            response = e
        self.assertEqual(response.code, 400)

    @gen_test
    def test_rooms_8(self):
        self._app.db = Mock()
        url = self.get_url('/hotels/1/rooms/1')
        request = HTTPRequest(url=url, method='PUT', body=json_encode({'room_number': 43}))
        try:
            response = yield self.http_client.fetch(request)
        except Exception as e:
            response = e
        self.assertEqual(response.code, 400)

    @gen_test
    def test_rooms_9(self):
        # Prepare mocks
        cursor_mock = mock_db_execute(self._app)
        cursor_mock.fetchone = lambda: (1, 11, 1, 1)

        # Run operation
        url = self.get_url('/hotels/1/rooms/1')
        request = HTTPRequest(url=url, method='DELETE')
        response = yield self.http_client.fetch(request)
        self.assertEqual(response.code, 200)
        self.assertEqual(json_decode(response.body), {'id': 1, 'room_number': 11, 'hotel_id': 1, 'floor_number': 1})
