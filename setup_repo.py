#!/usr/bin/env python3
"""
setup_repo.py
Ejecutar UNA SOLA VEZ en la raiz del proyecto.
Crea todas las carpetas, archivos base y configura git.

Uso:
    python setup_repo.py
"""

import os
import subprocess
import sys

BASE = os.getcwd()

# ─── Colores para la consola ──────────────────────────────────
OK   = "\033[92m✓\033[0m"
ERR  = "\033[91m✗\033[0m"
INFO = "\033[94m→\033[0m"

def run(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd or BASE,
                            capture_output=True, text=True)
    return result.returncode == 0, result.stdout.strip(), result.stderr.strip()

# ─── 1. Carpetas del proyecto ─────────────────────────────────
CARPETAS = [
    "bancos/banco_01_union",
    "bancos/banco_02_mercantil",
    "bancos/banco_03_bnb",
    "bancos/banco_04_bcp",
    "bancos/banco_05_bisa",
    "bancos/banco_06_ganadero",
    "bancos/banco_07_economico",
    "bancos/banco_08_prodem",
    "bancos/banco_09_solidario",
    "bancos/banco_10_fortaleza",
    "bancos/banco_11_fie",
    "bancos/banco_12_pyme",
    "bancos/banco_13_desarrollo",
    "bancos/banco_14_nacion_arg",
    "asfi/services",
    "asfi/routes",
    "crypto",
    "keys/certs",
    "logs",
    "sql",
    "neo4j",
    "config",
    "scripts",
    "tests/unit",
    "tests/integration",
]

# ─── 2. Archivos .gitkeep (para que git trackee carpetas vacías)
GITKEEP = [
    "keys/certs/.gitkeep",
    "logs/.gitkeep",
]

# ─── 3. __init__.py vacíos ────────────────────────────────────
INIT_PY = [
    "bancos/__init__.py",
    "bancos/banco_01_union/__init__.py",
    "bancos/banco_02_mercantil/__init__.py",
    "bancos/banco_03_bnb/__init__.py",
    "bancos/banco_04_bcp/__init__.py",
    "bancos/banco_05_bisa/__init__.py",
    "bancos/banco_06_ganadero/__init__.py",
    "bancos/banco_07_economico/__init__.py",
    "bancos/banco_08_prodem/__init__.py",
    "bancos/banco_09_solidario/__init__.py",
    "bancos/banco_10_fortaleza/__init__.py",
    "bancos/banco_11_fie/__init__.py",
    "bancos/banco_12_pyme/__init__.py",
    "bancos/banco_13_desarrollo/__init__.py",
    "bancos/banco_14_nacion_arg/__init__.py",
    "asfi/__init__.py",
    "asfi/services/__init__.py",
    "asfi/routes/__init__.py",
    "crypto/__init__.py",
    "config/__init__.py",
    "tests/__init__.py",
    "tests/unit/__init__.py",
    "tests/integration/__init__.py",
]

# ─── 4. .gitignore ────────────────────────────────────────────
GITIGNORE = """\
# === SECRETOS — NUNCA subir al repo ===
config/.env
keys/keys.json
keys/certs/*.pem
keys/certs/*.key
keys/*.json
!keys/keys.json.example
*serviceAccountKey.json
firebase_credentials.json

# === Logs generados en ejecucion ===
logs/*.log
logs/*.txt

# === Python ===
venv/
.venv/
__pycache__/
*.py[cod]
*.pyo
.pytest_cache/
*.egg-info/
dist/
build/

# === IDEs ===
.vscode/
.idea/
*.swp

# === OS ===
.DS_Store
Thumbs.db
"""

# ─── 5. README minimo ─────────────────────────────────────────
README = """\
# Plataforma ASFI — Conversion Monetaria Distribuida

## Equipo
| Nombre | Rol |
|---|---|
| Andy | PM |
| Samuel | BDs relacionales + APIs |
| Erika | Criptografia + Seguridad |
| Jose Gabriel | NoSQL + ASFI central |

## Setup rapido
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\\Scripts\\activate         # Windows
pip install -r requirements.txt
cp config/.env.example config/.env
# Editar config/.env con tus credenciales
python scripts/generate_keys.py
python scripts/generate_dataset.py
```

## Estructura
```
asfi-project/
├── bancos/          14 microservicios (uno por banco)
├── asfi/            Plataforma central ASFI
├── crypto/          Modulo de cifrado/descifrado
├── keys/            Llaves criptograficas (en .gitignore)
├── logs/            Archivos de auditoria
├── sql/             8 consultas SQL
├── neo4j/           Scripts del grafo
├── config/          Variables de entorno
└── scripts/         Utilitarios
```
"""

# ─── 6. requirements.txt ─────────────────────────────────────
REQUIREMENTS = """\
fastapi==0.111.0
uvicorn[standard]==0.29.0
pycryptodome==3.20.0
python-jose[cryptography]==3.3.0
aiohttp==3.9.5
sqlalchemy==2.0.30
psycopg2-binary==2.9.9
pymysql==1.1.1
pyodbc==5.1.0
pymongo==4.7.3
firebase-admin==6.5.0
neo4j==5.20.0
apscheduler==3.10.4
python-dotenv==1.0.1
cryptography==42.0.8
httpx==0.27.0
pydantic==2.7.1
"""

# ─── 7. .env.example ─────────────────────────────────────────
ENV_EXAMPLE = """\
# Copiar como config/.env y completar. NUNCA subir config/.env al repo.

JWT_SECRET_KEY=cambia_esto_por_una_clave_segura
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=5

PG_HOST=localhost
PG_PORT=5432
PG_USER=asfi_user
PG_PASSWORD=
PG_DB_UNION=banco_union
PG_DB_MERCANTIL=banco_mercantil
PG_DB_BNB=banco_bnb

SQLSERVER_HOST=localhost
SQLSERVER_PORT=1433
SQLSERVER_USER=sa
SQLSERVER_PASSWORD=
SQLSERVER_DB_BCP=banco_bcp
SQLSERVER_DB_BISA=banco_bisa
SQLSERVER_DB_GANADERO=banco_ganadero

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=asfi_user
MYSQL_PASSWORD=
MYSQL_DB_ECONOMICO=banco_economico
MYSQL_DB_PRODEM=banco_prodem
MYSQL_DB_SOLIDARIO=banco_solidario

MONGO_URI=mongodb://localhost:27017
MONGO_DB_FORTALEZA=banco_fortaleza
MONGO_DB_FIE=banco_fie
MONGO_DB_PYME=banco_pyme

FIREBASE_CREDENTIALS_PATH=keys/firebase_credentials.json
FIREBASE_PROJECT_ID=asfi-project

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=

PG_ASFI_HOST=localhost
PG_ASFI_PORT=5432
PG_ASFI_USER=asfi_central
PG_ASFI_PASSWORD=
PG_ASFI_DB=asfi_central

BCB_TC_BASE=6.9600
BCB_TC_VARIACION_MAX=0.9999
BCB_TC_INTERVALO_MINUTOS=3
"""

# ─────────────────────────────────────────────────────────────
# EJECUCION
# ─────────────────────────────────────────────────────────────

def main():
    print()
    print("=" * 52)
    print("  Setup inicial — Plataforma ASFI")
    print("=" * 52)

    # 1. Carpetas
    print(f"\n{INFO} Creando carpetas...")
    for carpeta in CARPETAS:
        ruta = os.path.join(BASE, carpeta)
        os.makedirs(ruta, exist_ok=True)
        print(f"   {OK} {carpeta}/")

    # 2. .gitkeep
    print(f"\n{INFO} Creando .gitkeep en carpetas vacias...")
    for archivo in GITKEEP:
        ruta = os.path.join(BASE, archivo)
        with open(ruta, "w") as f:
            f.write("")
        print(f"   {OK} {archivo}")

    # 3. __init__.py
    print(f"\n{INFO} Creando __init__.py...")
    for archivo in INIT_PY:
        ruta = os.path.join(BASE, archivo)
        if not os.path.exists(ruta):
            with open(ruta, "w") as f:
                f.write("")
        print(f"   {OK} {archivo}")

    # 4. Archivos raiz
    print(f"\n{INFO} Creando archivos base...")

    archivos = {
        ".gitignore":             GITIGNORE,
        "README.md":              README,
        "requirements.txt":       REQUIREMENTS,
        "config/.env.example":    ENV_EXAMPLE,
    }
    for nombre, contenido in archivos.items():
        ruta = os.path.join(BASE, nombre)
        if not os.path.exists(ruta):
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)
            print(f"   {OK} {nombre}")
        else:
            print(f"   → {nombre} ya existe, no se sobreescribe")

    # 5. keys.json.example
    keys_example = os.path.join(BASE, "keys", "keys.json.example")
    if not os.path.exists(keys_example):
        with open(keys_example, "w") as f:
            f.write('{\n  "_nota": "Copiar como keys.json. NUNCA subir keys.json al repo."\n}\n')
        print(f"   {OK} keys/keys.json.example")

    # 6. Git init
    print(f"\n{INFO} Configurando Git...")
    if not os.path.exists(os.path.join(BASE, ".git")):
        ok, _, _ = run("git init")
        if ok:
            run("git branch -m main")
            print(f"   {OK} Repositorio git inicializado (rama: main)")
        else:
            print(f"   {ERR} Error al inicializar git")
    else:
        print(f"   → Git ya inicializado")

    # 7. Commit inicial
    print(f"\n{INFO} Haciendo commit inicial...")
    run('git config user.email "asfi-team@proyecto.bo"')
    run('git config user.name "ASFI Team"')
    run("git add .")
    ok, out, err = run('git commit -m "chore: estructura inicial del proyecto ASFI"')
    if ok:
        print(f"   {OK} Commit inicial creado")
    else:
        if "nothing to commit" in err or "nothing to commit" in out:
            print(f"   → Nada nuevo para commitear")
        else:
            print(f"   {ERR} {err}")

    # 8. Resumen
    print()
    print("=" * 52)
    print("  LISTO")
    print("=" * 52)
    print(f"""
Proximos pasos:

  1. Conectar al repo remoto (GitHub/GitLab):
     git remote add origin <URL_DEL_REPO>
     git push -u origin main

  2. Cada miembro clona y configura:
     git clone <URL>
     pip install -r requirements.txt
     cp config/.env.example config/.env
     # Editar config/.env con sus credenciales

  3. Andy genera las llaves (UNA sola vez):
     python scripts/generate_keys.py

  4. Andy genera el dataset:
     python scripts/generate_dataset.py

  5. Cada quien trabaja en su rama:
     git checkout -b feature/samuel-dbs
     git checkout -b feature/erika-crypto
     git checkout -b feature/jose-nosql
     git checkout -b feature/andy-pm

IMPORTANTE:
  - Nunca subir config/.env ni keys/keys.json
  - El .gitignore ya los excluye automaticamente
""")

if __name__ == "__main__":
    main()