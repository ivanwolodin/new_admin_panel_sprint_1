from constansts import db_dataclasses_structure
from db_connections import open_sqlite_connection
from uploader import PostgresSaver


class DataTransfer:
    def __init__(self):
        self._chunk_size = 1000
        self.postgres_saver_obj = PostgresSaver()

    def transfer_data(self) -> None:
        for db_dataclass in db_dataclasses_structure:
            res = []
            temp = {}
            with open_sqlite_connection() as cursor:
                cursor.execute(
                    'SELECT * FROM {0} ORDER BY {1};'.format(
                        db_dataclass.get('sqlite_table'),
                        db_dataclass.get('order_by'),
                    ),
                )

                while chunks := cursor.fetchmany(self._chunk_size):
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
