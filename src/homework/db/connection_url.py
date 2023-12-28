import os
from dotenv import load_dotenv

config = load_dotenv()


def get_postgres_db_url() -> str:
    db = os.environ["POSTGRES_DB"]
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    host = os.environ["HOST"]
    return f"postgresql+psycopg2://{user}:{password}@{host}:5432/{db}"
