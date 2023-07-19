"""Dataclasses for each rows in each table."""
import inspect
from dataclasses import dataclass
from datetime import date
from typing import List, Optional
from uuid import UUID


@dataclass(frozen=True)
class Row:
    """A dataclass to represent a row in tables."""

    id: UUID
    created: str

    @classmethod
    def from_dict(cls, env: dict):
        """Generate Row from dictionary, adds created column.

        Args:
            env (dict): Original dictionary

        Returns:
            _type_: Row
        """
        filtered_dict = {
            k: v for k, v in env.items() if k in inspect.signature(cls).parameters
        }
        filtered_dict["created"] = "now()"
        return cls(**filtered_dict)


@dataclass(frozen=True)
class FilmWork(Row):
    title: str
    description: Optional[str]
    creation_date: Optional[date]
    rating: Optional[float]
    type: str
    source_name = "film_work"
    target_name = "content.film_work"


@dataclass(frozen=True)
class Genre(Row):
    name: str
    description: Optional[str]
    source_name = "genre"
    target_name = "content.genre"


@dataclass(frozen=True)
class Person(Row):
    full_name: str
    source_name = "person"
    target_name = "content.person"


@dataclass(frozen=True)
class GenreFilmWork(Row):
    film_work_id: UUID
    genre_id: UUID
    source_name = "genre_film_work"
    target_name = "content.genre_film_work"


@dataclass(frozen=True)
class PersonFilmWork(Row):
    film_work_id: UUID
    person_id: UUID
    role: Optional[str]
    source_name = "person_film_work"
    target_name = "content.person_film_work"


def get_models() -> List[type]:
    """Function to return all models to iterate over them.

    Returns:
        List[type]: List of models
    """
    return [FilmWork, Genre, Person, GenreFilmWork, PersonFilmWork]
