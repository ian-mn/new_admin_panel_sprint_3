# Generated by Django 4.2.2 on 2023-06-25 22:30

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class DateTimeWithoutTZField(models.DateTimeField):
    def db_type(self, connection):
        return "timestamp"


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL("create schema if not exists content;"),
        migrations.CreateModel(
            name="Filmwork",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", DateTimeWithoutTZField(auto_now_add=True)),
                ("modified", DateTimeWithoutTZField(auto_now=True)),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "description",
                    models.TextField(null=True, blank=True, verbose_name="description"),
                ),
                (
                    "creation_date",
                    models.DateField(null=True, verbose_name="creation_date"),
                ),
                (
                    "rating",
                    models.FloatField(
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="rating",
                    ),
                ),
                (
                    "type",
                    models.TextField(
                        choices=[("movie", "movie"), ("tv_show", "tv_show")],
                        verbose_name="type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Filmwork",
                "verbose_name_plural": "Filmworks",
                "db_table": 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", DateTimeWithoutTZField(auto_now_add=True)),
                ("modified", DateTimeWithoutTZField(auto_now=True)),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "description",
                    models.TextField(null=True, blank=True, verbose_name="description"),
                ),
            ],
            options={
                "verbose_name": "Genre",
                "verbose_name_plural": "Genres",
                "db_table": 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", DateTimeWithoutTZField(auto_now_add=True)),
                ("modified", DateTimeWithoutTZField(auto_now=True)),
                (
                    "full_name",
                    models.CharField(max_length=255, verbose_name="full_name"),
                ),
            ],
            options={
                "verbose_name": "Person",
                "verbose_name_plural": "Persons",
                "db_table": 'content"."person',
            },
        ),
        migrations.CreateModel(
            name="PersonFilmWork",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "role",
                    models.TextField(
                        choices=[
                            ("actor", "actor"),
                            ("director", "director"),
                            ("writer", "writer"),
                        ],
                        verbose_name="role",
                    ),
                ),
                ("created", DateTimeWithoutTZField(auto_now_add=True)),
                (
                    "film_work",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movies.filmwork",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movies.person",
                        verbose_name="Person",
                    ),
                ),
            ],
            options={
                "verbose_name": "PersonFilmWork",
                "verbose_name_plural": "PersonFilmWorks",
                "db_table": 'content"."person_film_work',
            },
        ),
        migrations.CreateModel(
            name="GenreFilmWork",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", DateTimeWithoutTZField(auto_now_add=True)),
                (
                    "film_work",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movies.filmwork",
                    ),
                ),
                (
                    "genre",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movies.genre",
                        verbose_name="Genre",
                    ),
                ),
            ],
            options={
                "verbose_name": "GenreFilmWork",
                "verbose_name_plural": "GenreFilmWorks",
                "db_table": 'content"."genre_film_work',
            },
        ),
        migrations.AddField(
            model_name="filmwork",
            name="genres",
            field=models.ManyToManyField(
                through="movies.GenreFilmWork", to="movies.genre"
            ),
        ),
        migrations.AddField(
            model_name="filmwork",
            name="persons",
            field=models.ManyToManyField(
                through="movies.PersonFilmWork", to="movies.person"
            ),
        ),
        migrations.AddConstraint(
            model_name="genrefilmwork",
            constraint=models.UniqueConstraint(
                fields=("genre", "film_work"), name="genre_film_work_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="personfilmwork",
            constraint=models.UniqueConstraint(
                fields=("film_work", "person", "role"), name="film_work_person_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="filmwork",
            index=models.Index(
                fields=["rating", "creation_date"], name="rating_create_date_idx"
            ),
        ),
        migrations.RunSQL(
            'ALTER TABLE "content".film_work ALTER COLUMN modified DROP NOT NULL;'
        ),
        migrations.RunSQL(
            'ALTER TABLE "content".genre ALTER COLUMN modified DROP NOT NULL;'
        ),
        migrations.RunSQL(
            'ALTER TABLE "content".person ALTER COLUMN modified DROP NOT NULL;'
        ),
    ]
