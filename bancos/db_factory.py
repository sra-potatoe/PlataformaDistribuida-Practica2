"""bancos/db_factory.py — Fábrica de conexiones SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import (PG_HOST, PG_PORT, PG_USER, PG_PASSWORD,
                              SS_HOST, SS_PORT, SS_USER, SS_PASSWORD, SS_DRIVER,
                              MY_HOST, MY_PORT, MY_USER, MY_PASSWORD)

_engines = {}

def _url(motor: str, db: str) -> str:
    if motor == "pg":
        return f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{db}"
    if motor == "ss":
        drv = SS_DRIVER.replace(" ", "+")
        return f"mssql+pyodbc://{SS_USER}:{SS_PASSWORD}@{SS_HOST}:{SS_PORT}/{db}?driver={drv}&TrustServerCertificate=yes"
    if motor == "my":
        return f"mysql+pymysql://{MY_USER}:{MY_PASSWORD}@{MY_HOST}:{MY_PORT}/{db}"
    raise ValueError(f"Motor desconocido: {motor}")

def get_engine(motor: str, db: str):
    key = f"{motor}:{db}"
    if key not in _engines:
        _engines[key] = create_engine(_url(motor, db), pool_pre_ping=True, echo=False)
    return _engines[key]

def get_session(motor: str, db: str):
    return sessionmaker(bind=get_engine(motor, db))()
