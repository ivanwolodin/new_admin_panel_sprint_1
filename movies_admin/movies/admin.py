from django.contrib import admin
from .models import Genre, FilmWork


# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    pass
