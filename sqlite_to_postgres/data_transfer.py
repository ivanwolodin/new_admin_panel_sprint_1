import sqlite3

from psycopg2.extensions import connection as _connection

from constansts import db_dataclasses_structure
from uploader import PostgresSaver


class DataTransfer:
    def __init__(self, connection: sqlite3.Connection, pg_conn: _connection):
        self._conn = connection
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()
        self._chunk_size = 100
        self.postgres_saver_obj = PostgresSaver(pg_conn)

    def transfer_data(self) -> None:
        for db_dataclass in db_dataclasses_structure:
            res = []
            temp = {}
            self._cursor.execute(
                'SELECT * FROM {0} ORDER BY {1};'.format(
                    db_dataclass.get('sqlite_table'),
                    db_dataclass.get('order_by'),
                    ),
                )

            while True:
                chunks = self._cursor.fetchmany(self._chunk_size)
                if not chunks:
                    break

                for chunk in chunks:
                    dict_chunk = dict(chunk)
                    for row_field in db_dataclass.get('fields'):
                        temp[row_field] = dict_chunk[row_field]

                    res.append(
                        db_dataclass.get('dataclass')(**temp),
                    )

                self.postgres_saver_obj.save_data(
                    {
                        'res': res,
                        'postgres_table': db_dataclass.get('postgres_table'),
                    },
                )

                res.clear()
                temp.clear()
