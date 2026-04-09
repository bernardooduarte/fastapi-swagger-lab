from sqlalchemy import text
from sqlmodel import SQLModel, Session, create_engine

DATABASE_NAME = "accounts"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "postgres"
DATABASE_HOST = "localhost"
DATABASE_PORT = 5432

ADMIN_DATABASE_URL = (
    f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/postgres"
)
DATABASE_URL = (
    f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)


def _ensure_database_exists() -> None:
    admin_engine = create_engine(ADMIN_DATABASE_URL, isolation_level="AUTOCOMMIT")

    try:
        with admin_engine.connect() as connection:
            result = connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :database_name"),
                {"database_name": DATABASE_NAME},
            ).scalar()

            if not result:
                connection.execute(text(f'CREATE DATABASE "{DATABASE_NAME}"'))
    finally:
        admin_engine.dispose()


_ensure_database_exists()

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    from app.models import AccountDB, UserDB

    SQLModel.metadata.create_all(engine)