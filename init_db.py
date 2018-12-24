import argparse
import os
import logging

import psycopg2

logger = logging.getLogger(__name__)


def init_db(db_name, db_user, db_pass, db_host, db_port, path_to_sql_files):
    logger.info('Initializing database for application.')
    dsn = 'dbname={} user={} password={} host={} port={}'.format(db_name, db_user, db_pass, db_host, db_port)
    conn = psycopg2.connect(dsn=dsn)
    cursor = conn.cursor()
    try:
        for file in os.listdir(path_to_sql_files):
            full_file_path = os.path.join(path_to_sql_files, file)
            cursor.execute(open(full_file_path, 'r').read())
    except Exception as e:
        logger.error(e)
    else:
        logger.info('Successfully initialized database for application.')
    finally:
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--dbhost', default='/var/run/postgresql/', required=False,
                             help='Host where PostgreSQL is located.')
    args_parser.add_argument('--dbport', default=5432, required=False, help='PostgreSQL PORT.')
    args_parser.add_argument('--dbuser', default='frutkic', required=False, help='DB user name.')
    args_parser.add_argument('--dbname', default='hotel', required=False, help='DB name.')
    args_parser.add_argument('--dbpass', default='1111', required=False, help='DB user pass.')
    args_parser.add_argument('--path', default='db/schema', required=False, help='Path to directory with sql schemas.')
    args = args_parser.parse_args()
    init_db(args.dbname, args.dbuser, args.dbpass, args.dbhost, args.dbport, args.path)
