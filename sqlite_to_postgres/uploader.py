from db_connections import open_postgres_connection
from logger import logger

class PostgresSaver:
    def __init__(self):
        self._data_to_upload = []

        self._function_by_table = {
            'film_work': self._upload_film_works,
            'genre': self._upload_genres,
            'person': self._upload_persons,
            'genre_film_work': self._upload_genre_film_works,
            'person_film_work': self._upload_person_film_works,
        }

    def _upload_film_works(self):
        with open_postgres_connection() as pg_cursor:
            args = ','.join(
                pg_cursor.mogrify('(%s, %s, %s, %s, %s, %s, %s, %s)',
                    (item.id,
                     item.title,
                     item.description,
                     item.creation_date,
                     item.rating,
                     item.type,
                     item.created_at,
                     item.updated_at),
                    ).decode()
                for item in self._data_to_upload
            )
            pg_cursor.execute(f"""
                                INSERT INTO content.film_work (
                                 id,
                                 title,
                                 description,
                                 creation_date,
                                 rating,
                                 type,
                                 created,
                                 modified
                                ) 
                                VALUES {args}
                                ON CONFLICT (id) DO NOTHING """)

    def _upload_persons(self):
        with open_postgres_connection() as pg_cursor:
            args = ','.join(
                pg_cursor.mogrify('(%s, %s, %s, %s)', 
                                     (item.id, 
                                      item.full_name, 
                                      item.created_at,
                                      item.updated_at)).decode() 
                for item in self._data_to_upload
            )
            pg_cursor.execute(f"""
                                INSERT INTO content.person (
                                 id, 
                                 full_name, 
                                 created, 
                                 modified
                                ) 
                                VALUES {args}
                                ON CONFLICT (id) DO NOTHING """)

    def _upload_genres(self):
        with open_postgres_connection() as pg_cursor:
            args = ','.join(
                pg_cursor.mogrify('(%s, %s, %s, %s, %s)', 
                                     (item.id, 
                                      item.name, 
                                      item.description, 
                                      item.created_at,
                                      item.updated_at)).decode() 
                for item in self._data_to_upload
            )
            pg_cursor.execute(f"""
                                INSERT INTO content.genre (
                                 id, 
                                 name, 
                                 description,
                                 created, 
                                 modified
                                ) 
                                VALUES {args}
                                ON CONFLICT (id) DO NOTHING """)

    def _upload_person_film_works(self):
        with open_postgres_connection() as pg_cursor:
            args = ','.join(
                pg_cursor.mogrify('(%s, %s, %s, %s, %s)', 
                                     (item.id, 
                                      item.film_work_id, 
                                      item.person_id, 
                                      item.created_at,
                                      item.role)).decode() 
                for item in self._data_to_upload
            )
            pg_cursor.execute(f"""
                                INSERT INTO content.person_film_work (
                                 id, 
                                 film_work_id, 
                                 person_id,
                                 created, 
                                 role
                                ) 
                                VALUES {args}
                                ON CONFLICT (id) DO NOTHING """)


    def _upload_genre_film_works(self):
        with open_postgres_connection() as pg_cursor:
            args = ','.join(
                pg_cursor.mogrify('(%s, %s, %s, %s)', 
                                     (item.id, 
                                      item.genre_id, 
                                      item.film_work_id, 
                                      item.created_at,
                                      )).decode() 
                for item in self._data_to_upload
            )
            pg_cursor.execute(f"""
                                INSERT INTO content.genre_film_work (
                                 id, 
                                 genre_id, 
                                 film_work_id,
                                 created
                                ) 
                                VALUES {args}
                                ON CONFLICT (id) DO NOTHING """)

    def save_data(self, data: dict) -> bool:
        self._data_to_upload = data['res']
        try:
            logger.info(
                'Inserting chunk into: {0}'.format(data['postgres_table']),
            )
            self._function_by_table[data['postgres_table']]()
        except Exception as e:
            logger.info('Cannot upsert data: Error: {0}'.format(e))
