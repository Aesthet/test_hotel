from entities_managers.base_manager import BaseManager


class HotelManager(BaseManager):

    queries_map = {
        'get_all': """SELECT * FROM hotels;""",
        'create': """INSERT INTO hotels (name) VALUES (%s) RETURNING *;""",
        'get_one': """SELECT * FROM hotels WHERE id=%s;""",
        'update': """UPDATE hotels SET name=%s WHERE id=%s RETURNING *;""",
        'delete': """DELETE FROM hotels WHERE id=%s RETURNING *;"""
    }
