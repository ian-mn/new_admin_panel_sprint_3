from model import Movie


def transform(batch: list) -> list[dict]:
    """Transforms rows from PostgreSQL to Elasticsearch bulk actions.

    Args:
    batch (List): List of rows from PostgreSQL.

    Returns:
        list[dict]: Bulk query text.
    """
    movies_batch = [Movie.parse_obj(row) for row in batch]
    bulk_actions = [
        {"_index": "movies", "_id": row.id, "_source": row.json()}
        for row in movies_batch
    ]
    return bulk_actions
