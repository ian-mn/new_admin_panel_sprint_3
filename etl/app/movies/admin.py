from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmWork, Person, PersonFilmWork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "id")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("full_name", "id")


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (
        GenreFilmworkInline,
        PersonFilmWorkInline,
    )

    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
        "get_genres",
    )

    list_prefetch_related = ("genres",)

    def get_queryset(self, request):
        queryset = (
            super().get_queryset(request).prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = "Жанры фильма"

    list_filter = ("type",)
    search_fields = ("title", "description", "id")
