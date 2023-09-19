import os
import pytest
import psycopg2
import sqlite3

from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

load_dotenv()

dsl = {
        'dbname': os.environ.get('DB_NAME'), 
        'user': os.environ.get('DB_USER'), 
        'password': os.environ.get('DB_PASSWORD'), 
        'host': os.environ.get('DB_HOST'), 
        'port': os.environ.get('DB_PORT'),
    }

database_names = [
    'film_work',
    'genre',
    'genre_film_work',
    'person_film_work',
    'person'
]

def fetch_pg_table_row_numbers(pg_conn: _connection, table_name: str):
    conn = pg_conn
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM content.{0};'.format(table_name))
    return cursor.fetchone()[0] 

def fetch_sql_table_row_numbers(sqlite_conn: sqlite3.Connection, table_name: str):
    conn = sqlite_conn
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM {0};'.format(table_name))
    return cursor.fetchone()[0]

@pytest.mark.parametrize("database_name",database_names)
def test_inserted_numbers(database_name):
    with sqlite3.connect('../db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        assert fetch_pg_table_row_numbers(pg_conn, database_name) == fetch_sql_table_row_numbers(sqlite_conn, database_name)
