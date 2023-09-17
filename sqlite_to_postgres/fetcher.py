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
        
    def _fetch_film_works(self) -> list:
        self._cursor.execute("SELECT * FROM film_work;")
        return [
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
            for movie in self._cursor.fetchall()
        ]

    def _fetch_persons(self) -> list:
        self._cursor.execute("SELECT * FROM person;")
        return [
            Person(
                full_name=person['full_name'],
                created_at=person['created_at'],
                updated_at=person['updated_at'],
                id=person['id'],
            ) 
            for person in self._cursor.fetchall()
        ]

    def _fetch_genres(self) -> list:
        self._cursor.execute("SELECT * FROM genre;")
        return [
            Genre(
                name=genre['name'],
                description=genre['description'],
                created_at=genre['created_at'],
                updated_at=genre['updated_at'],
                id=genre['id'],
            ) 
            for genre in self._cursor.fetchall()
        ]

    def _fetch_person_film_works(self) -> list:
        self._cursor.execute("SELECT * FROM person_film_work;")
        return [
            PersonFilmWork(
                role=person_film_work['role'],
                created_at=person_film_work['created_at'],
                id=person_film_work['id'],
                film_work_id=person_film_work['film_work_id'],
                person_id=person_film_work['person_id'],
            ) 
            for person_film_work in self._cursor.fetchall()
        ]

    def _fetch_genre_film_works(self) -> list:
        self._cursor.execute("SELECT * FROM genre_film_work;")
        return [
            GenreFilmWork(
                created_at=genre_film_work['created_at'],
                id=genre_film_work['id'],
                film_work_id=genre_film_work['film_work_id'],
                genre_id=genre_film_work['genre_id'],
            ) 
            for genre_film_work in self._cursor.fetchall()
        ]

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
            print('Cannot fetch data. Exception: {0}'.format(e))
