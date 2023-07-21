from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, validator


class Person(BaseModel):
    id: UUID
    name: str


class Movie(BaseModel):
    id: UUID
    imdb_rating: Optional[float]
    genre: List[str]
    title: str
    description: Optional[str]
    director: List[str]
    actors_names: List[str]
    writers_names: List[str]
    actors: Optional[List[Person]]
    writers: Optional[List[Person]]

    @validator("director", "actors_names", "writers_names", pre=True)
    def null_is_empty_list(cls, v, values, **kwargs):
        """If value is None sets it to an empty list."""
        if v:
            return v
        else:
            return []
