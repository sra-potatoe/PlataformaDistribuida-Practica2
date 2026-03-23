"""
scripts/barrido_paralelo.py
Barrido paralelo de los 14 bancos.
Mide tiempo secuencial vs paralelo y documenta speedup.

Uso:
    python -m scripts.barrido_paralelo
"""

import sys
import os
import time
import json
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

# Añadir raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from bancos.auth_jwt import crear_token

# ─── Configuración de bancos ─────────────────────────
BANCOS_APIS = [
    {"id": 1,  "nombre": "Unión",      "url": "https://localhost:8001"},
    {"id": 2,  "nombre": "Mercantil",   "url": "https://localhost:8002"},
    {"id": 3,  "nombre": "BNB",         "url": "https://localhost:8003"},
    {"id": 4,  "nombre": "BCP",         "url": "https://localhost:8004"},
    {"id": 5,  "nombre": "BISA",        "url": "https://localhost:8005"},
    {"id": 6,  "nombre": "Ganadero",    "url": "https://localhost:8006"},
    {"id": 7,  "nombre": "Económico",   "url": "https://localhost:8007"},
    {"id": 8,  "nombre": "Prodem",      "url": "https://localhost:8008"},
    {"id": 9,  "nombre": "Solidario",   "url": "https://localhost:8009"},
    # Estos los levantará otro equipo:
    # {"id": 10, "nombre": "Fortaleza",   "url": "https://localhost:8010"},
    # {"id": 11, "nombre": "FIE",         "url": "https://localhost:8011"},
    # {"id": 12, "nombre": "PYME",        "url": "https://localhost:8012"},
    # {"id": 13, "nombre": "Desarrollo",  "url": "https://localhost:8013"},
    # {"id": 14, "nombre": "Nación Arg",  "url": "https://localhost:8014"},
]

import uuid

def consultar_banco(banco: dict) -> dict:
    """Consulta un banco y retorna el resultado con tiempo."""
    t0 = time.perf_counter()
    try:
        token = crear_token(banco["id"])
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Nonce": str(uuid.uuid4()),
            "X-Timestamp": str(time.time()),
        }
        with httpx.Client(verify=False, timeout=30.0) as client:
            resp = client.get(f"{banco['url']}/cuentas?limit=100", headers=headers)
            cuentas = resp.json() if resp.status_code == 200 else []
        elapsed = time.perf_counter() - t0
        return {
            "banco_id": banco["id"],
            "nombre": banco["nombre"],
            "cuentas_obtenidas": len(cuentas),
            "tiempo_s": round(elapsed, 4),
            "status": resp.status_code,
        }
    except Exception as e:
        elapsed = time.perf_counter() - t0
        return {
            "banco_id": banco["id"],
            "nombre": banco["nombre"],
            "cuentas_obtenidas": 0,
            "tiempo_s": round(elapsed, 4),
            "error": str(e),
        }


def main():
    print("=" * 60)
    print("  BARRIDO PARALELO — Plataforma ASFI")
    print("=" * 60)

    bancos_activos = [b for b in BANCOS_APIS]
    n = len(bancos_activos)
    print(f"\nBancos a consultar: {n}")

    # ─── SECUENCIAL ──────────────────────────────────
    print("\n--- Modo SECUENCIAL ---")
    t0_sec = time.perf_counter()
    resultados_sec = [consultar_banco(b) for b in bancos_activos]
    t_secuencial = time.perf_counter() - t0_sec

    for r in resultados_sec:
        status = r.get("error", f"OK ({r['cuentas_obtenidas']} cuentas)")
        print(f"  Banco {r['banco_id']:2d} ({r['nombre']:12s}): {r['tiempo_s']:.4f}s — {status}")
    print(f"\n  TOTAL secuencial: {t_secuencial:.4f}s")

    # ─── PARALELO ────────────────────────────────────
    print("\n--- Modo PARALELO (ThreadPoolExecutor) ---")
    t0_par = time.perf_counter()
    with ThreadPoolExecutor(max_workers=14) as pool:
        futuros = {pool.submit(consultar_banco, b): b for b in bancos_activos}
        resultados_par = []
        for futuro in as_completed(futuros):
            resultados_par.append(futuro.result())
    t_paralelo = time.perf_counter() - t0_par

    resultados_par.sort(key=lambda x: x["banco_id"])
    for r in resultados_par:
        status = r.get("error", f"OK ({r['cuentas_obtenidas']} cuentas)")
        print(f"  Banco {r['banco_id']:2d} ({r['nombre']:12s}): {r['tiempo_s']:.4f}s — {status}")
    print(f"\n  TOTAL paralelo:   {t_paralelo:.4f}s")

    # ─── SPEEDUP ─────────────────────────────────────
    speedup = t_secuencial / t_paralelo if t_paralelo > 0 else 0
    print(f"\n{'=' * 60}")
    print(f"  SPEEDUP: {speedup:.2f}x")
    print(f"  Secuencial: {t_secuencial:.4f}s")
    print(f"  Paralelo:   {t_paralelo:.4f}s")
    print(f"  Ahorro:     {t_secuencial - t_paralelo:.4f}s")
    print(f"{'=' * 60}")

    # ─── Guardar resultados ──────────────────────────
    log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs", "barrido_resultados.txt")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n{'=' * 60}\n")
        f.write(f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n")
        f.write(f"Bancos consultados: {n}\n")
        f.write(f"Secuencial: {t_secuencial:.4f}s\n")
        f.write(f"Paralelo:   {t_paralelo:.4f}s\n")
        f.write(f"Speedup:    {speedup:.2f}x\n")
        f.write(f"Resultados: {json.dumps(resultados_par, ensure_ascii=False, default=str)}\n")
    print(f"\nResultados guardados en: {log_path}")


if __name__ == "__main__":
    main()
