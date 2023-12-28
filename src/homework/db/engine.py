import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

config = load_dotenv()


def get_postgres_db_url() -> str:
    db = os.environ.get("POSTGRES_DB", "")
    user = os.environ.get("POSTGRES_USER", "")
    password = os.environ.get("POSTGRES_PASSWORD", "")
    host = os.environ.get("HOST", "")
    return f"postgresql+psycopg2://{user}:{password}@{host}:5432/{db}"


engine = create_engine(get_postgres_db_url())
