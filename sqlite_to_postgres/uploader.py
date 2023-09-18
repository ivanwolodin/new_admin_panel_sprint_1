import sys

from psycopg2.extensions import connection as _connection

class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self._conn = pg_conn
        self._cursor = self._conn.cursor()
        self._data_to_upload = dict()
    
    def _upload_film_works(self):
        try:
            items = self._data_to_upload['film_work']
            args = ','.join(
                self._cursor.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s)", 
                                     (item.id, 
                                      item.title, 
                                      item.description, 
                                      item.creation_date, 
                                      item.rating, 
                                      item.type, 
                                      item.created_at,
                                      item.updated_at)).decode() 
                for item in items
            )
            self._cursor.execute(f"""
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
            self._conn.commit()
        except Exception as e:
            print("Cannot upsert in film_works. Error: {0}".format(e))
            self._conn.rollback()
            self._conn.close()
            
    def _upload_persons(self):
        try:
            items = self._data_to_upload['person']
            args = ','.join(
                self._cursor.mogrify("(%s, %s, %s, %s)", 
                                     (item.id, 
                                      item.full_name, 
                                      item.created_at,
                                      item.updated_at)).decode() 
                for item in items
            )
            self._cursor.execute(f"""
                                INSERT INTO content.person (
                                 id, 
                                 full_name, 
                                 created, 
                                 modified
                                ) 
                                VALUES {args}
                                ON CONFLICT (id) DO NOTHING """)
            self._conn.commit()
        except Exception as e:
            print("Cannot upsert in person. Error: {0}".format(e))
            self._conn.rollback()
            self._conn.close()

    def _upload_genres(self):
        try:
            items = self._data_to_upload['genre']
            args = ','.join(
                self._cursor.mogrify("(%s, %s, %s, %s, %s)", 
                                     (item.id, 
                                      item.name, 
                                      item.description, 
                                      item.created_at,
                                      item.updated_at)).decode() 
                for item in items
            )
            self._cursor.execute(f"""
                                INSERT INTO content.genre (
                                 id, 
                                 name, 
                                 description,
                                 created, 
                                 modified
                                ) 
                                VALUES {args}
                                ON CONFLICT (id) DO NOTHING """)
            self._conn.commit()
        except Exception as e:
            print("Cannot upsert in genre. Error: {0}".format(e))
            self._conn.rollback()
            self._conn.close()

    def _upload_person_film_works(self):
        try:
            items = self._data_to_upload['person_film_work']
            args = ','.join(
                self._cursor.mogrify("(%s, %s, %s, %s, %s)", 
                                     (item.id, 
                                      item.film_work_id, 
                                      item.person_id, 
                                      item.created_at,
                                      item.role)).decode() 
                for item in items
            )
            self._cursor.execute(f"""
                                INSERT INTO content.person_film_work (
                                 id, 
                                 film_work_id, 
                                 person_id,
                                 created, 
                                 role
                                ) 
                                VALUES {args}
                                ON CONFLICT (id) DO NOTHING """)
            self._conn.commit()
        except Exception as e:
            print("Cannot upsert in person_film_work. Error: {0}".format(e))
            self._conn.rollback()
            self._conn.close()

    def _upload_genre_film_works(self):
        try:
            items = self._data_to_upload['genre_film_work']
            args = ','.join(
                self._cursor.mogrify("(%s, %s, %s, %s)", 
                                     (item.id, 
                                      item.genre_id, 
                                      item.film_work_id, 
                                      item.created_at
                                      )).decode() 
                for item in items
            )
            self._cursor.execute(f"""
                                INSERT INTO content.genre_film_work (
                                 id, 
                                 genre_id, 
                                 film_work_id,
                                 created
                                ) 
                                VALUES {args}
                                ON CONFLICT (id) DO NOTHING """)
            self._conn.commit()
        except Exception as e:
            print("Cannot upsert in genre_film_work. Error: {0}".format(e))
            self._conn.rollback()
            self._conn.close()

    def save_all_data(self, data: dict) -> bool:
        self._data_to_upload = data
        try:
            self._upload_film_works()
            self._upload_persons()
            self._upload_genres()
            self._upload_person_film_works()
            self._upload_genre_film_works()
        except Exception as e:
            print('Cannot upsert data: Error: {0}'.format(e))
