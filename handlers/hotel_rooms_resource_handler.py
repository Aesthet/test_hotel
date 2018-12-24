from tornado import web
from tornado import gen
from tornado.escape import (
    json_decode,
    json_encode
)

from entities_managers import RoomManager

KEYS = ['id', 'room_number', 'hotel_id', 'floor_number', 'guest_name']


class HotelRoomsHandler(web.RequestHandler):

    @gen.coroutine
    def get(self, hotel_id):
        all_rooms = yield RoomManager(self.application.db).get_all(hotel_id)
        result = [dict(zip(KEYS, hotel)) for hotel in all_rooms]
        self.write(json_encode(result))

    @gen.coroutine
    def post(self, hotel_id):
        args = json_decode(self.request.body)
        try:
            room_number = args['room_number']
            floor_number = args['floor_number']
        except KeyError:
            raise web.HTTPError(400)
        new_room = yield RoomManager(self.application.db).create(hotel_id, room_number, floor_number)
        self.write(json_encode(dict(zip(KEYS, new_room))))


class HotelRoomHandler(web.RequestHandler):

    @gen.coroutine
    def get(self, hotel_id, room_id):
        room = yield RoomManager(self.application.db).get_one(room_id)
        try:
            result = json_encode(dict(zip(KEYS, room)))
            self.write(result)
        except TypeError:
            raise web.HTTPError(404)

    @gen.coroutine
    def put(self, hotel_id, room_id):
        args = json_decode(self.request.body)
        try:
            room_number = args['room_number']
            floor_number = args['floor_number']
        except KeyError:
            raise web.HTTPError(400)
        room = yield RoomManager(self.application.db).update(room_number, floor_number, room_id)
        try:
            result = json_encode(dict(zip(KEYS, room)))
            self.write(result)
        except TypeError:
            raise web.HTTPError(404)

    @gen.coroutine
    def delete(self, hotel_id, room_id):
        room = yield RoomManager(self.application.db).delete(room_id)
        try:
            result = json_encode(dict(zip(KEYS, room)))
            self.write(result)
        except TypeError:
            raise web.HTTPError(404)
