"""
config/settings.py — Configuración centralizada.
Uso: from config.settings import PG_HOST, BANCOS_CONFIG
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# ─── JWT ─────────────────────────────────────────────
JWT_SECRET_KEY  = os.getenv("JWT_SECRET_KEY", "dev_key")
JWT_ALGORITHM   = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MIN  = int(os.getenv("JWT_EXPIRE_MINUTES", "5"))

# ─── PostgreSQL ──────────────────────────────────────
PG_HOST     = os.getenv("PG_HOST", "localhost")
PG_PORT     = os.getenv("PG_PORT", "5432")
PG_USER     = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")
PG_DB_UNION     = os.getenv("PG_DB_UNION", "banco_union")
PG_DB_MERCANTIL = os.getenv("PG_DB_MERCANTIL", "banco_mercantil")
PG_DB_BNB       = os.getenv("PG_DB_BNB", "banco_bnb")

# ─── SQL Server ──────────────────────────────────────
SS_HOST     = os.getenv("SQLSERVER_HOST", "localhost")
SS_PORT     = os.getenv("SQLSERVER_PORT", "1433")
SS_USER     = os.getenv("SQLSERVER_USER", "sa")
SS_PASSWORD = os.getenv("SQLSERVER_PASSWORD", "")
SS_DRIVER   = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 17 for SQL Server")
SS_DB_BCP      = os.getenv("SQLSERVER_DB_BCP", "banco_bcp")
SS_DB_BISA     = os.getenv("SQLSERVER_DB_BISA", "banco_bisa")
SS_DB_GANADERO = os.getenv("SQLSERVER_DB_GANADERO", "banco_ganadero")

# ─── MySQL ───────────────────────────────────────────
MY_HOST     = os.getenv("MYSQL_HOST", "localhost")
MY_PORT     = os.getenv("MYSQL_PORT", "3306")
MY_USER     = os.getenv("MYSQL_USER", "root")
MY_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MY_DB_ECONOMICO = os.getenv("MYSQL_DB_ECONOMICO", "banco_economico")
MY_DB_PRODEM    = os.getenv("MYSQL_DB_PRODEM", "banco_prodem")
MY_DB_SOLIDARIO = os.getenv("MYSQL_DB_SOLIDARIO", "banco_solidario")

# ─── MongoDB ─────────────────────────────────────────
MONGO_URI          = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_FORTALEZA = os.getenv("MONGO_DB_FORTALEZA", "banco_fortaleza")
MONGO_DB_FIE       = os.getenv("MONGO_DB_FIE", "banco_fie")
MONGO_DB_PYME      = os.getenv("MONGO_DB_PYME", "banco_pyme")

# ─── Firebase ────────────────────────────────────────
FIREBASE_CRED = os.getenv("FIREBASE_CREDENTIALS_PATH", "keys/firebase_credentials.json")
FIREBASE_PROJ = os.getenv("FIREBASE_PROJECT_ID", "asfi-project")

# ─── Neo4j ───────────────────────────────────────────
NEO4J_URI  = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASSWORD", "")

# ─── ASFI Central ────────────────────────────────────
ASFI_HOST = os.getenv("PG_ASFI_HOST", "localhost")
ASFI_PORT = os.getenv("PG_ASFI_PORT", "5432")
ASFI_USER = os.getenv("PG_ASFI_USER", "postgres")
ASFI_PASS = os.getenv("PG_ASFI_PASSWORD", "")
ASFI_DB   = os.getenv("PG_ASFI_DB", "asfi_central")

# ─── Tipo de Cambio ──────────────────────────────────
TC_BASE     = float(os.getenv("BCB_TC_BASE", "6.96"))
TC_VAR_MAX  = float(os.getenv("BCB_TC_VARIACION_MAX", "0.9999"))
TC_INTERVAL = int(os.getenv("BCB_TC_INTERVALO_MINUTOS", "3"))
HMAC_KEY    = os.getenv("HMAC_SECRET_KEY", "hmac_dev_key")

# ─── SSL ─────────────────────────────────────────────
SSL_CERT = os.getenv("SSL_CERTFILE", "keys/certs/server.pem")
SSL_KEY  = os.getenv("SSL_KEYFILE", "keys/certs/server.key")

# ─── Mapeo de bancos ─────────────────────────────────
BANCOS = {
    1:  {"nombre": "Banco Unión S.A.",                  "algo": "cesar",     "motor": "pg",    "db": PG_DB_UNION,       "port": 8001, "cuentas": 22472},
    2:  {"nombre": "Banco Mercantil Santa Cruz S.A.",   "algo": "atbash",    "motor": "pg",    "db": PG_DB_MERCANTIL,   "port": 8002, "cuentas": 19975},
    3:  {"nombre": "Banco Nacional de Bolivia S.A.",    "algo": "vigenere",  "motor": "pg",    "db": PG_DB_BNB,         "port": 8003, "cuentas": 14981},
    4:  {"nombre": "Banco de Crédito de Bolivia S.A.",  "algo": "playfair",  "motor": "ss",    "db": SS_DB_BCP,         "port": 8004, "cuentas": 13983},
    5:  {"nombre": "Banco BISA S.A.",                   "algo": "hill",      "motor": "ss",    "db": SS_DB_BISA,        "port": 8005, "cuentas": 10487},
    6:  {"nombre": "Banco Ganadero S.A.",               "algo": "des",       "motor": "ss",    "db": SS_DB_GANADERO,    "port": 8006, "cuentas": 9488},
    7:  {"nombre": "Banco Económico S.A.",              "algo": "3des",      "motor": "my",    "db": MY_DB_ECONOMICO,   "port": 8007, "cuentas": 8489},
    8:  {"nombre": "Banco Prodem S.A.",                 "algo": "blowfish",  "motor": "my",    "db": MY_DB_PRODEM,      "port": 8008, "cuentas": 7491},
    9:  {"nombre": "Banco Solidario S.A.",              "algo": "twofish",   "motor": "my",    "db": MY_DB_SOLIDARIO,   "port": 8009, "cuentas": 5493},
    10: {"nombre": "Banco Fortaleza S.A.",              "algo": "aes",       "motor": "mongo", "db": MONGO_DB_FORTALEZA, "port": 8010, "cuentas": 3496},
    11: {"nombre": "Banco FIE S.A.",                    "algo": "rsa",       "motor": "mongo", "db": MONGO_DB_FIE,      "port": 8011, "cuentas": 3995},
    12: {"nombre": "Banco PYME de la Comunidad S.A.",   "algo": "elgamal",   "motor": "mongo", "db": MONGO_DB_PYME,     "port": 8012, "cuentas": 2247},
    13: {"nombre": "Banco de Desarrollo Productivo",    "algo": "ecc",       "motor": "fire",  "db": "banco_desarrollo","port": 8013, "cuentas": 999},
    14: {"nombre": "Banco de la Nación Argentina",      "algo": "chacha20",  "motor": "fire",  "db": "banco_nacion_arg","port": 8014, "cuentas": 200},
}
