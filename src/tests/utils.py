from functools import wraps

import sqlalchemy

from src.app.db_config import DATABASE_URL


def db_reset():
    """Reset test database after running a function."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            engine = sqlalchemy.create_engine(DATABASE_URL)
            connection = engine.connect()
            truncate_query = sqlalchemy.text("TRUNCATE TABLE url")
            connection.execution_options(autocommit=True).execute(truncate_query)
        return wrapper
    return decorator
