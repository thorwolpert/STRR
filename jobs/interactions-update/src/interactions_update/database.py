import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Global singleton to hold the pooled engine
_engine = None


def get_engine():
    """Lazily initialize the pooled engine with recycling and pooling."""
    global _engine
    if _engine is not None:
        return _engine

    url = os.getenv("DATABASE_URL")

    # 1. Determine pool size based on workers (default to 10)
    workers = int(os.getenv("MAX_WORKERS", "10"))

    # Pool Configuration
    pool_params = {
        "pool_size": workers,
        "max_overflow": 5,
        "pool_pre_ping": True,  # Verifies connection is alive before use
        "pool_recycle": 3600,  # Recycle connections after 1 hour
        "pool_timeout": 30,  # Seconds to wait for a connection from the pool
    }

    # Testcontainer - if running tests
    if url:
        _engine = create_engine(url, **pool_params)
        return _engine

    # Google Cloud SQL
    from google.cloud.sql.connector import Connector
    from google.cloud.sql.connector import IPTypes

    instance_conn = os.getenv("INSTANCE_CONNECTION_NAME")
    db_user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")

    if not all([instance_conn, db_user, db_name]):
        raise ValueError("Missing Cloud SQL connection environment variables.")

    connector = Connector()

    def get_conn():
        return connector.connect(
            instance_conn,
            "pg8000",
            user=db_user,
            db=db_name,
            enable_iam_auth=True,
            ip_type=IPTypes.PUBLIC,
        )

    # Apply pooling params to the creator-based engine
    _engine = create_engine("postgresql+pg8000://", creator=get_conn, **pool_params)
    return _engine


def get_session():
    """Generator for sessions using the singleton engine pool."""
    engine = get_engine()
    # expire_on_commit=False prevents issues when accessing objects
    # after a thread has committed but before the session closes.
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory() as session:
        yield session
