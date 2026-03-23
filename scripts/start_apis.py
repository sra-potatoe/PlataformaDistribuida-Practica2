"""
scripts/start_apis.py
Levanta todas las APIs de bancos en paralelo (una por proceso).

Uso:
    python -m scripts.start_apis
"""

import subprocess
import sys
import os
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APIS = [
    {"module": "bancos.banco_01_union.app",      "port": 8001, "nombre": "Unión"},
    {"module": "bancos.banco_02_mercantil.app",   "port": 8002, "nombre": "Mercantil"},
    {"module": "bancos.banco_03_bnb.app",         "port": 8003, "nombre": "BNB"},
    {"module": "bancos.banco_04_bcp.app",         "port": 8004, "nombre": "BCP"},
    {"module": "bancos.banco_05_bisa.app",        "port": 8005, "nombre": "BISA"},
    {"module": "bancos.banco_06_ganadero.app",    "port": 8006, "nombre": "Ganadero"},
    {"module": "bancos.banco_07_economico.app",   "port": 8007, "nombre": "Económico"},
    {"module": "bancos.banco_08_prodem.app",      "port": 8008, "nombre": "Prodem"},
    {"module": "bancos.banco_09_solidario.app",   "port": 8009, "nombre": "Solidario"},
]

SSL_CERT = os.path.join(BASE, "keys", "certs", "server.pem")
SSL_KEY = os.path.join(BASE, "keys", "certs", "server.key")


def main():
    print("=" * 50)
    print("  Iniciando APIs de bancos")
    print("=" * 50)

    procesos = []
    for api in APIS:
        cmd = [
            sys.executable, "-m", "uvicorn",
            f"{api['module']}:app",
            "--host", "0.0.0.0",
            "--port", str(api["port"]),
            "--ssl-certfile", SSL_CERT,
            "--ssl-keyfile", SSL_KEY,
        ]
        print(f"  → Puerto {api['port']}: {api['nombre']}")
        proc = subprocess.Popen(cmd, cwd=BASE)
        procesos.append(proc)
        time.sleep(0.3)

    print(f"\n✓ {len(procesos)} APIs iniciadas")
    print("  Presiona Ctrl+C para detener todas\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo APIs...")
        for p in procesos:
            p.terminate()
        for p in procesos:
            p.wait()
        print("Todas detenidas.")


if __name__ == "__main__":
    main()
