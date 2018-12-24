from tornado import web
from tornado import gen
from tornado.escape import (
    json_decode,
    json_encode
)

from entities_managers import HotelManager

KEYS = ['id', 'name']


class HotelsHandler(web.RequestHandler):

    @gen.coroutine
    def get(self):
        all_hotels = yield HotelManager(self.application.db).get_all()
        result = [dict(zip(KEYS, hotel)) for hotel in all_hotels]
        self.write(json_encode(result))

    @gen.coroutine
    def post(self):
        args = json_decode(self.request.body)
        try:
            hotel_name = args['name']
        except KeyError:
            raise web.HTTPError(400)
        new_hotel = yield HotelManager(self.application.db).create(hotel_name)
        self.write(json_encode(dict(zip(KEYS, new_hotel))))


class HotelHandler(web.RequestHandler):

    @gen.coroutine
    def get(self, hotel_id):
        hotel = yield HotelManager(self.application.db).get_one(hotel_id)
        try:
            result = json_encode(dict(zip(KEYS, hotel)))
            self.write(result)
        except TypeError:
            raise web.HTTPError(404)

    @gen.coroutine
    def put(self, hotel_id):
        args = json_decode(self.request.body)
        try:
            new_name = args['name']
        except KeyError:
            raise web.HTTPError(400)
        hotel = yield HotelManager(self.application.db).update(new_name, hotel_id)
        try:
            result = json_encode(dict(zip(KEYS, hotel)))
            self.write(result)
        except TypeError:
            raise web.HTTPError(404)

    @gen.coroutine
    def delete(self, hotel_id):
        hotel = yield HotelManager(self.application.db).delete(hotel_id)
        try:
            result = json_encode(dict(zip(KEYS, hotel)))
            self.write(result)
        except TypeError:
            raise web.HTTPError(404)
