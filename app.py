import argparse

import momoko

from handlers.hotel_resource import (
    HotelHandler,
    HotelsHandler
)

from handlers.hotel_rooms_resource import (
    HotelRoomHandler,
    HotelRoomsHandler
)

from handlers.booking_resource import BookingResource
from tornado import (
    ioloop,
    web,
    httpserver
)


def get_handlers():
    handlers = [
        (r'/hotels/?', HotelsHandler),
        (r'/hotels/([0-9]+)/?', HotelHandler),
        (r'/hotels/([0-9]+)/rooms/?', HotelRoomsHandler),
        (r'/hotels/([0-9]+)/rooms/([0-9]+)/?', HotelRoomHandler),
        (r'/hotels/([0-9]+)/rooms/([0-9]+)/book/?', BookingResource)
    ]
    return handlers


def make_app():
    handlers = get_handlers()
    app = web.Application(handlers, autoreload=True, debug=True)
    return app


def run(host, port, db_name, db_user, db_pass, db_host, db_port):
    app = make_app()
    loop = ioloop.IOLoop.instance()
    dsn = 'dbname={} user={} password={} host={} port={}'.format(db_name, db_user, db_pass, db_host, db_port)
    app.db = momoko.Pool(dsn=dsn, size=1, ioloop=loop)
    future = app.db.connect()
    loop.add_future(future, lambda f: loop.stop())
    loop.start()
    future.result()
    server = httpserver.HTTPServer(app)
    server.listen(port, host)
    loop.start()


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-H', '--host', default='localhost', required=False, help='Host to run app on.')
    args_parser.add_argument('-P', '--port', default=8080, required=False, help='Port to run app on.')
    args_parser.add_argument('--dbhost', default='/var/run/postgresql/', required=False,
                             help='Host where PostgreSQL is located.')
    args_parser.add_argument('--dbport', default=5432, required=False, help='PostgreSQL PORT.')
    args_parser.add_argument('--dbuser', default='frutkic', required=False, help='DB user name.')
    args_parser.add_argument('--dbname', default='hotel', required=False, help='DB name.')
    args_parser.add_argument('--dbpass', default='1111', required=False, help='DB user pass.')
    args = args_parser.parse_args()
    run(args.host, args.port, args.dbname, args.dbuser, args.dbpass, args.dbhost, args.dbport)
