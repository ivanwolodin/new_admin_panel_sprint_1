# Create your models here.
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Genre(models.Model):

    def __str__(self):
        return self.name

    # Типичная модель в Django использует число в качестве id.
    # В таких ситуациях поле не описывается в модели.

    # Вам же придётся явно объявить primary key.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField('name', max_length=255)

    # blank=True делает поле необязательным для заполнения.
    description = models.TextField('description', blank=True)

    # auto_now_add автоматически выставит дату создания записи
    created = models.DateTimeField(auto_now_add=True)

    # auto_now изменятся при каждом обновлении записи
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме.
        # Это нужно указать в классе модели

        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class FilmWork(models.Model):

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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('title', max_length=255)
    description = models.TextField('description', blank=True)
    creation_date = models.DateField('creation_date')
    rating = models.FloatField(
        'rating',
        validators=[validate_interval],
        blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    type = models.CharField('type', choices=MoviesType.choices, max_length=7)

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'
