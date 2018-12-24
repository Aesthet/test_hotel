from tornado import gen
from mock import Mock


def mock_db_execute(application):
    cursor_mock = Mock()
    application.db = Mock()
    application.db.execute = Mock()
    application.db.execute.side_effect = [gen.maybe_future(cursor_mock)]
    return cursor_mock
