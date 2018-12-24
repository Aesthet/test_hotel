from entities_managers.base_manager import BaseManager


class BookingManager(BaseManager):

    queries_map = {
        'create': """INSERT INTO booking (room_id, guest_name) VALUES (%s, %s) RETURNING *;""",
        'update': """UPDATE booking SET guest_name=%s WHERE room_id=%s RETURNING *;""",
        'delete': """DELETE FROM booking WHERE room_id=%s RETURNING *;"""
    }
