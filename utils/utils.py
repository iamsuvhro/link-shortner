import os
from dotenv import load_dotenv


def mongo_config():
    load_dotenv()
    client = os.getenv("CLIENT")
    db = os.getenv("DB")
    collection = os.getenv("COLLECTION")

    if not client or not db or not collection:
        raise ValueError(
            "Missing one or more required environment variables: CLIENT, DB, COLLECTION")

    return {
        "client": client,
        "db": db,
        "collection": collection,
    }
