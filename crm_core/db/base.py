from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker, Session
from crm_core.config.settings import settings

# Importar todos os modelos para garantir que sejam registrados
from crm_core.db import models  # noqa: F401

# Usar NullPool para SQLite (melhor para aplicações web)
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    poolclass=NullPool  # Sem pool de conexões para SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def dispose_engine():
    """Descarta todas as conexões do pool."""
    engine.dispose()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session() -> Session:
    """Retorna uma nova sessão do banco de dados."""
    return SessionLocal()
