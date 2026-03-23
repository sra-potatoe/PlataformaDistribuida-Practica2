"""
bancos/db_factory.py
Fábrica centralizada de conexiones SQLAlchemy.
Cada API de banco importa:
    from bancos.db_factory import get_engine, get_session
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import (
    PG_HOST, PG_PORT, PG_USER, PG_PASSWORD,
    SQLSERVER_HOST, SQLSERVER_PORT, SQLSERVER_USER, SQLSERVER_PASSWORD, SQLSERVER_DRIVER,
    MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD,
)

# Cache de engines (un engine por BD, reutilizable)
_engines = {}


def _build_url(motor: str, db_name: str) -> str:
    """Construye la URL de conexión según el motor."""
    if motor == "postgresql":
        return f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{db_name}"
    elif motor == "sqlserver":
        driver = SQLSERVER_DRIVER.replace(" ", "+")
        return (
            f"mssql+pyodbc://{SQLSERVER_USER}:{SQLSERVER_PASSWORD}"
            f"@{SQLSERVER_HOST}:{SQLSERVER_PORT}/{db_name}"
            f"?driver={driver}&TrustServerCertificate=yes"
        )
    elif motor == "mysql":
        return f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{db_name}"
    else:
        raise ValueError(f"Motor no soportado: {motor}")


def get_engine(motor: str, db_name: str):
    """Retorna un Engine SQLAlchemy, creándolo solo la primera vez."""
    key = f"{motor}:{db_name}"
    if key not in _engines:
        url = _build_url(motor, db_name)
        _engines[key] = create_engine(url, pool_pre_ping=True, echo=False)
    return _engines[key]


def get_session(motor: str, db_name: str):
    """Retorna una Session SQLAlchemy nueva."""
    engine = get_engine(motor, db_name)
    Session = sessionmaker(bind=engine)
    return Session()
