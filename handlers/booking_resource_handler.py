from tornado import web
from tornado import gen
from tornado.escape import (
    json_decode,
    json_encode
)

from entities_managers import BookingManager


KEYS = ['room_id', 'guest_name']


class BookingResource(web.RequestHandler):

    @gen.coroutine
    def post(self, hotel_id, room_id):
        args = json_decode(self.request.body)
        try:
            guest_name = args['guest_name']
        except KeyError:
            raise web.HTTPError(400)
        new_booking = yield BookingManager(self.application.db).create(room_id, guest_name)
        self.write(json_encode(dict(zip(KEYS, new_booking))))

    @gen.coroutine
    def put(self, hotel_id, room_id):
        args = json_decode(self.request.body)
        try:
            guest_name = args['guest_name']
        except KeyError:
            raise web.HTTPError(400)
        booking = yield BookingManager(self.application.db).update(guest_name, room_id)
        try:
            result = json_encode(dict(zip(KEYS, booking)))
            self.write(result)
        except TypeError:
            raise web.HTTPError(404)

    @gen.coroutine
    def delete(self, hotel_id, room_id):
        booking = yield BookingManager(self.application.db).delete(room_id)
        try:
            result = json_encode(dict(zip(KEYS, booking)))
            self.write(result)
        except TypeError:
            raise web.HTTPError(404)
