import sqlite3

from models import (
    FilmWork,
    Genre,
    GenreFilmWork,
    Person,
    PersonFilmWork,
)

class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()
        self._chunk_size = 100
        
    def _fetch_film_works(self) -> list:
        res = []
        try:
            self._cursor.execute("SELECT * FROM film_work ORDER BY creation_date;")
            while True:
                movies = self._cursor.fetchmany(self._chunk_size)
                if not movies:
                    break
                else:
                    for movie in movies:
                        res.append(
                            FilmWork(
                                rating=movie['rating'],
                                id=movie['id'],
                                title=movie['title'],
                                description=movie['description'],
                                file_path=movie['file_path'],
                                type=movie['type'],
                                creation_date=movie['creation_date'],
                                created_at=movie['created_at'],
                                updated_at=movie['updated_at'],
                            ) 
                        )
        except Exception as e:
            print('Cannot fetch film_work. Error: {0}'.format(e))
        finally:
            return res

    def _fetch_persons(self) -> list:
        res = []
        try:
            self._cursor.execute("SELECT * FROM person ORDER BY created_at;")
            while True:
                persons = self._cursor.fetchmany(self._chunk_size)
                if not persons:
                    break
                else:
                    for person in persons:
                        res.append(
                            Person(
                                full_name=person['full_name'],
                                created_at=person['created_at'],
                                updated_at=person['updated_at'],
                                id=person['id'],
                            ) 
                        )
            return res
        except Exception as e:
            print('Cannot fetch person. Error: {0}'.format(e))
        finally: 
            return res

    def _fetch_genres(self) -> list:
        res = []
        try:
            self._cursor.execute("SELECT * FROM genre ORDER BY created_at;")
            while True:
                genres = self._cursor.fetchmany(self._chunk_size)
                if not genres:
                    break
                else:
                    for genre in genres:
                        res.append(
                            Genre(
                                name=genre['name'],
                                description=genre['description'],
                                created_at=genre['created_at'],
                                updated_at=genre['updated_at'],
                                id=genre['id'],
                            )  
                        )
        except Exception as e:
            print('Cannot fetch genre. Error: {0}'.format(e))
        finally: 
            return res

    def _fetch_person_film_works(self) -> list:
        res = []
        try:
            self._cursor.execute("SELECT * FROM person_film_work ORDER BY created_at;")
            while True:
                person_film_works = self._cursor.fetchmany(self._chunk_size)
                if not person_film_works:
                    break
                else:
                    for person_film_work in person_film_works:
                        res.append(
                            PersonFilmWork(
                                role=person_film_work['role'],
                                created_at=person_film_work['created_at'],
                                id=person_film_work['id'],
                                film_work_id=person_film_work['film_work_id'],
                                person_id=person_film_work['person_id'],
                            )
                        )
        except Exception as e:
            print('Cannot fetch person_film_work. Error: {0}'.format(e))
        finally: 
            return res

    def _fetch_genre_film_works(self) -> list:
        
        res = []
        try:
            self._cursor.execute("SELECT * FROM genre_film_work ORDER BY created_at;")
            while True:
                genre_film_works = self._cursor.fetchmany(self._chunk_size)
                if not genre_film_works:
                    break
                else:
                    for genre_film_work in genre_film_works:
                        res.append(
                            GenreFilmWork(
                                created_at=genre_film_work['created_at'],
                                id=genre_film_work['id'],
                                film_work_id=genre_film_work['film_work_id'],
                                genre_id=genre_film_work['genre_id'],
                            ) 
                        )
            
        except Exception as e:
            print('Cannot fetch genre_film_work. Error: {0}'.format(e))
        finally: 
            return res

    def extract_movies(self) -> dict:
        try:
            return {
                'film_work': self._fetch_film_works(),
                'genre': self._fetch_genres(),
                'person': self._fetch_persons(),
                'genre_film_work': self._fetch_genre_film_works(),
                'person_film_work': self._fetch_person_film_works(),
            }
        except Exception as e:
            # TODO: add logger instead of print()
            print('Cannot fetch data. Exception: {0}'.format(e))
