import os

import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from dotenv import load_dotenv

from fetcher import SQLiteExtractor
from uploader import PostgresSaver 

load_dotenv()

def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    data = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('DB_NAME'), 
        'user': os.environ.get('DB_USER'), 
        'password': os.environ.get('DB_PASSWORD'), 
        'host': os.environ.get('DB_HOST'), 
        'port': os.environ.get('DB_PORT'),
    }
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
