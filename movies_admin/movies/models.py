# Create your models here.
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, 
        # что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):

    def __str__(self):
        return self.name

    name = models.CharField('name', max_length=255)

    # blank=True делает поле необязательным для заполнения.
    description = models.TextField('description', blank=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме.
        # Это нужно указать в классе модели

        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class FilmWork(UUIDMixin, TimeStampedMixin):
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    def __str__(self):
        return self.title

    def validate_interval(value):
        min_value = 0.0
        max_value = 10.0
        if value < min_value or value > max_value:
            raise ValidationError(
                _('%(value)s должно быть в диапазоне [{0}, {1}]'.format(
                    min_value,
                    max_value)),
                params={'value': value})

    class MoviesType(models.TextChoices):
        MOVIES = 'MOVIES'
        TV_SHOW = 'TV_SHOW'

    title = models.CharField('title', max_length=255)
    description = models.TextField('description', blank=True)
    creation_date = models.DateField('creation_date')
    rating = models.FloatField(
        'rating',
        validators=[validate_interval],
        blank=True)
    type = models.CharField('type', choices=MoviesType.choices, max_length=7)

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField('full_name', max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField('role', null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
