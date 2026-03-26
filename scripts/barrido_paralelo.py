"""
scripts/barrido_paralelo.py — Barrido paralelo de 14 bancos.
Mide secuencial vs paralelo, documenta speedup.
Uso: python -m scripts.barrido_paralelo
"""
import sys, os, time, json, uuid
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from bancos.auth_jwt import crear_token

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APIS = [{"id": i, "nombre": n, "url": f"https://localhost:{p}"}
        for i, n, p in [
    (1,"Unión",8001),(2,"Mercantil",8002),(3,"BNB",8003),(4,"BCP",8004),
    (5,"BISA",8005),(6,"Ganadero",8006),(7,"Económico",8007),(8,"Prodem",8008),
    (9,"Solidario",8009),
    # Agregar cuando estén listos:
    # (10,"Fortaleza",8010),(11,"FIE",8011),(12,"PYME",8012),(13,"Desarrollo",8013),(14,"Nación",8014),
]]

def consultar(b):
    t0 = time.perf_counter()
    try:
        h = {"Authorization": f"Bearer {crear_token(b['id'])}", "X-Nonce": str(uuid.uuid4()), "X-Timestamp": str(time.time())}
        with httpx.Client(verify=False, timeout=30) as c:
            r = c.get(f"{b['url']}/cuentas?limit=100", headers=h)
            n = len(r.json()) if r.status_code == 200 else 0
        return {"id": b["id"], "nombre": b["nombre"], "cuentas": n, "t": round(time.perf_counter()-t0, 4), "ok": True}
    except Exception as e:
        return {"id": b["id"], "nombre": b["nombre"], "cuentas": 0, "t": round(time.perf_counter()-t0, 4), "error": str(e)}

def main():
    print("="*55+"\n  BARRIDO PARALELO — ASFI\n"+"="*55)
    # Secuencial
    t0 = time.perf_counter()
    res_s = [consultar(b) for b in APIS]
    ts = time.perf_counter() - t0
    for r in res_s: print(f"  [{r['t']:.3f}s] Banco {r['id']:2d} {r['nombre']:12s} — {r.get('error','OK')}")
    print(f"  TOTAL SEC: {ts:.4f}s\n")
    # Paralelo
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=14) as pool:
        res_p = sorted([f.result() for f in as_completed([pool.submit(consultar, b) for b in APIS])], key=lambda x: x["id"])
    tp = time.perf_counter() - t0
    for r in res_p: print(f"  [{r['t']:.3f}s] Banco {r['id']:2d} {r['nombre']:12s} — {r.get('error','OK')}")
    sp = ts / tp if tp > 0 else 0
    print(f"\n{'='*55}\n  SEC={ts:.4f}s  PAR={tp:.4f}s  SPEEDUP={sp:.2f}x\n{'='*55}")
    # Log
    lp = os.path.join(BASE, "logs", "barrido_resultados.txt")
    os.makedirs(os.path.dirname(lp), exist_ok=True)
    with open(lp, "a") as f:
        f.write(f"\n{datetime.now(timezone.utc).isoformat()} SEC={ts:.4f} PAR={tp:.4f} SP={sp:.2f}x\n")
    print(f"  Log: {lp}")

if __name__ == "__main__":
    main()
