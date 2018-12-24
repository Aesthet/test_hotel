from tornado import gen


class BaseManager(object):
    queries_map = {}

    def __init__(self, db_client):
        self.db_client = db_client

    @gen.coroutine
    def create(self, *args):
        query = self.queries_map['create']
        conn = self.db_client.execute(query, args)
        yield conn
        cursor = conn.result()
        raise gen.Return(cursor.fetchone())

    @gen.coroutine
    def get_all(self, *args):
        query = self.queries_map['get_all']
        conn = self.db_client.execute(query, args)
        yield conn
        cursor = conn.result()
        raise gen.Return(cursor.fetchall())

    @gen.coroutine
    def get_one(self, *args):
        query = self.queries_map['get_one']
        conn = self.db_client.execute(query, args)
        yield conn
        cursor = conn.result()
        raise gen.Return(cursor.fetchone())

    @gen.coroutine
    def update(self, *args):
        query = self.queries_map['update']
        conn = self.db_client.execute(query, args)
        yield conn
        cursor = conn.result()
        raise gen.Return(cursor.fetchone())

    @gen.coroutine
    def delete(self, *args):
        query = self.queries_map['delete']
        conn = self.db_client.execute(query, args)
        yield conn
        cursor = conn.result()
        raise gen.Return(cursor.fetchone())
