import logging
from typing import Dict, List

from backoff import backoff
from elasticsearch import Elasticsearch, helpers
from queries.index import MAPPINGS, SETTINGS
from settings import get_settings


class Load:
    INDEX = "movies"

    def __init__(self) -> None:
        es_settings = get_settings().es
        url = f"http://{es_settings.host}:{es_settings.port}"
        self.es = Elasticsearch(url)
        self.__load_index()

    @backoff()
    def __load_index(self) -> None:
        """Loads index into Elasticsearch."""
        if not self.es.indices.exists(index=self.INDEX):
            logging.info(f"Creating ES index '{self.INDEX}'")
            self.es.indices.create(
                index=self.INDEX,
                mappings=MAPPINGS,
                settings=SETTINGS,
            )
        else:
            logging.info(f"ES index '{self.INDEX}' already exists.")

    @backoff()
    def bulk(self, actions: List[Dict]) -> None:
        """Bulk loads actions into Elasticsearch.

        Args:
            actions (List[Dict]): Bulk query.
        """
        logging.info("Bulk loading to Elasticsearch.")
        helpers.bulk(self.es, actions)
