"""
config/settings.py
Carga centralizada de variables de entorno.
Cada módulo importa lo que necesita:
    from config.settings import PG_HOST, JWT_SECRET_KEY, ...
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env desde config/
_env_path = Path(__file__).parent / ".env"
load_dotenv(_env_path)

# ─── JWT ─────────────────────────────────────────────
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_dev_key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "5"))

# ─── PostgreSQL (Bancos 1-3) ─────────────────────────
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")

PG_DB_UNION = os.getenv("PG_DB_UNION", "banco_union")
PG_DB_MERCANTIL = os.getenv("PG_DB_MERCANTIL", "banco_mercantil")
PG_DB_BNB = os.getenv("PG_DB_BNB", "banco_bnb")

# ─── SQL Server (Bancos 4-6) ─────────────────────────
SQLSERVER_HOST = os.getenv("SQLSERVER_HOST", "localhost")
SQLSERVER_PORT = os.getenv("SQLSERVER_PORT", "1433")
SQLSERVER_USER = os.getenv("SQLSERVER_USER", "sa")
SQLSERVER_PASSWORD = os.getenv("SQLSERVER_PASSWORD", "")
SQLSERVER_DRIVER = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 17 for SQL Server")

SQLSERVER_DB_BCP = os.getenv("SQLSERVER_DB_BCP", "banco_bcp")
SQLSERVER_DB_BISA = os.getenv("SQLSERVER_DB_BISA", "banco_bisa")
SQLSERVER_DB_GANADERO = os.getenv("SQLSERVER_DB_GANADERO", "banco_ganadero")

# ─── MySQL (Bancos 7-9) ──────────────────────────────
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

MYSQL_DB_ECONOMICO = os.getenv("MYSQL_DB_ECONOMICO", "banco_economico")
MYSQL_DB_PRODEM = os.getenv("MYSQL_DB_PRODEM", "banco_prodem")
MYSQL_DB_SOLIDARIO = os.getenv("MYSQL_DB_SOLIDARIO", "banco_solidario")

# ─── Firebase (Bancos 13-14) ─────────────────────────
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "keys/firebase_credentials.json")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "asfi-project")

# ─── ASFI Central ────────────────────────────────────
PG_ASFI_HOST = os.getenv("PG_ASFI_HOST", "localhost")
PG_ASFI_PORT = os.getenv("PG_ASFI_PORT", "5432")
PG_ASFI_USER = os.getenv("PG_ASFI_USER", "postgres")
PG_ASFI_PASSWORD = os.getenv("PG_ASFI_PASSWORD", "")
PG_ASFI_DB = os.getenv("PG_ASFI_DB", "asfi_central")

# ─── Tipo de Cambio ──────────────────────────────────
BCB_TC_BASE = float(os.getenv("BCB_TC_BASE", "6.9600"))
BCB_TC_VARIACION_MAX = float(os.getenv("BCB_TC_VARIACION_MAX", "0.9999"))
BCB_TC_INTERVALO_MINUTOS = int(os.getenv("BCB_TC_INTERVALO_MINUTOS", "3"))

# ─── SSL ─────────────────────────────────────────────
SSL_CERTFILE = os.getenv("SSL_CERTFILE", "keys/certs/server.pem")
SSL_KEYFILE = os.getenv("SSL_KEYFILE", "keys/certs/server.key")

# ─── Mapeo de bancos ─────────────────────────────────
BANCOS_CONFIG = {
    1:  {"nombre": "Banco Unión S.A.",                  "algoritmo": "cesar",     "motor": "postgresql", "db": PG_DB_UNION,        "puerto_api": 8001},
    2:  {"nombre": "Banco Mercantil Santa Cruz S.A.",   "algoritmo": "atbash",    "motor": "postgresql", "db": PG_DB_MERCANTIL,    "puerto_api": 8002},
    3:  {"nombre": "Banco Nacional de Bolivia S.A.",    "algoritmo": "vigenere",  "motor": "postgresql", "db": PG_DB_BNB,          "puerto_api": 8003},
    4:  {"nombre": "Banco de Crédito de Bolivia S.A.",  "algoritmo": "playfair",  "motor": "sqlserver",  "db": SQLSERVER_DB_BCP,   "puerto_api": 8004},
    5:  {"nombre": "Banco BISA S.A.",                   "algoritmo": "hill",      "motor": "sqlserver",  "db": SQLSERVER_DB_BISA,  "puerto_api": 8005},
    6:  {"nombre": "Banco Ganadero S.A.",               "algoritmo": "des",       "motor": "sqlserver",  "db": SQLSERVER_DB_GANADERO, "puerto_api": 8006},
    7:  {"nombre": "Banco Económico S.A.",              "algoritmo": "3des",      "motor": "mysql",      "db": MYSQL_DB_ECONOMICO, "puerto_api": 8007},
    8:  {"nombre": "Banco Prodem S.A.",                 "algoritmo": "blowfish",  "motor": "mysql",      "db": MYSQL_DB_PRODEM,    "puerto_api": 8008},
    9:  {"nombre": "Banco Solidario S.A.",              "algoritmo": "twofish",   "motor": "mysql",      "db": MYSQL_DB_SOLIDARIO, "puerto_api": 8009},
    13: {"nombre": "Banco de Desarrollo Productivo S.A.M.", "algoritmo": "ecc",   "motor": "firebase",   "db": "banco_desarrollo", "puerto_api": None},
    14: {"nombre": "Banco de la Nación Argentina",      "algoritmo": "chacha20",  "motor": "firebase",   "db": "banco_nacion_arg", "puerto_api": None},
}
