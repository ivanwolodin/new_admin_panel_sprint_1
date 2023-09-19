from dataclasses import fields

from models import (
    FilmWork,
    Genre,
    GenreFilmWork,
    Person,
    PersonFilmWork,
)

db_dataclasses_structure = (
    {
        'dataclass': FilmWork, 
        'order_by': 'created_at',
        'fields': [field.name for field in fields(FilmWork)],
        'sqlite_table': 'film_work',
        'postgres_table': 'film_work',
    },
    {
        'dataclass': Genre, 
        'order_by': 'created_at',
        'fields': [field.name for field in fields(Genre)],
        'sqlite_table': 'genre',
        'postgres_table': 'genre',
    },
    {
        'dataclass': Person, 
        'order_by': 'created_at',
        'fields': [field.name for field in fields(Person)],
        'sqlite_table': 'person',
        'postgres_table': 'person',
    },
    {
        'dataclass': GenreFilmWork, 
        'order_by': 'created_at',
        'fields': [field.name for field in fields(GenreFilmWork)],
        'sqlite_table': 'genre_film_work',
        'postgres_table': 'genre_film_work',
    },
    {
        'dataclass': PersonFilmWork, 
        'order_by': 'created_at',
        'fields': [field.name for field in fields(PersonFilmWork)],
        'sqlite_table': 'person_film_work',
        'postgres_table': 'person_film_work',
    },
)
