import os
from sqlalchemy.engine.url import URL

def get_db_config() -> dict:
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT"))
    db_name = os.getenv("DB_NAME")
    url = URL.create(
            drivername="postgresql+asyncpg",
            username=username,
            password=password,
            host=host,
            port=port,
            database=db_name
        )
    return {"url": url, "username": username, "password": password, "host": host, "port": port, "db_name": db_name}
