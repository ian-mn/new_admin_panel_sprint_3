from uuid import UUID

from pydantic import BaseModel, validator


class Person(BaseModel):
    id: UUID
    name: str


class Movie(BaseModel):
    id: UUID
    imdb_rating: float | None
    genre: list[str]
    title: str
    description: str | None
    director: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[Person] | None
    writers: list[Person] | None

    @validator("director", "actors_names", "writers_names", pre=True)
    def null_is_empty_list(cls, v, values, **kwargs):
        """If value is None sets it to an empty list."""
        if v:
            return v
        else:
            return []
