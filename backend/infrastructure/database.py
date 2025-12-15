"""Database configuration and session management."""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from config import settings


Base = declarative_base()


class Database:
    """Database connection manager with session pooling."""

    def __init__(self, url: str | None = None):
        self._url = url or settings.database_url
        self._engine = None
        self._session_factory = None

    @property
    def engine(self):
        """Lazy-load engine with connection pooling."""
        if self._engine is None:
            # SQLite-specific settings
            if self._url.startswith("sqlite"):
                self._engine = create_engine(
                    self._url,
                    connect_args={"check_same_thread": False},
                    pool_pre_ping=True,
                )
            else:
                # PostgreSQL/MySQL pooling settings
                self._engine = create_engine(
                    self._url,
                    pool_size=5,
                    max_overflow=10,
                    pool_pre_ping=True,
                    pool_recycle=300,
                )
        return self._engine

    @property
    def session_factory(self):
        """Lazy-load session factory."""
        if self._session_factory is None:
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
            )
        return self._session_factory

    def create_tables(self):
        """Create all tables."""
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """Provide a transactional scope around a series of operations."""
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


# Global database instance
db = Database()