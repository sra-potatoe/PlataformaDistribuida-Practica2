"""
asfi/services/tipo_cambio.py — Servicio de tipo de cambio BCB.
Simula fluctuación ±0.9999 cada 3 min con APScheduler.
Endpoint /tipo-cambio firmado con HMAC anti-tampering.

Uso independiente:  python -m asfi.services.tipo_cambio
"""
import hashlib, hmac, json, random, time
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from threading import Lock

from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import TC_BASE, TC_VAR_MAX, TC_INTERVAL, HMAC_KEY

app = FastAPI(title="Servicio Tipo de Cambio BCB", version="1.0.0")

# ─── Estado del tipo de cambio ───────────────────────
_lock = Lock()
_tc_actual = {
    "tipo_cambio": Decimal(str(TC_BASE)),
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "variacion": Decimal("0"),
}


def _generar_hmac(data: dict) -> str:
    """Firma HMAC-SHA256 del tipo de cambio para anti-tampering."""
    msg = f"{data['tipo_cambio']}|{data['timestamp']}".encode()
    return hmac.new(HMAC_KEY.encode(), msg, hashlib.sha256).hexdigest()


def _actualizar_tc():
    """Fluctúa el tipo de cambio ±0.9999 respecto al base."""
    with _lock:
        variacion = Decimal(str(random.uniform(-TC_VAR_MAX, TC_VAR_MAX)))
        variacion = variacion.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
        nuevo = Decimal(str(TC_BASE)) + variacion
        nuevo = nuevo.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
        _tc_actual["tipo_cambio"] = nuevo
        _tc_actual["variacion"] = variacion
        _tc_actual["timestamp"] = datetime.now(timezone.utc).isoformat()
    print(f"[TC] {_tc_actual['timestamp']} → {nuevo} (var: {variacion:+})")


# ─── Scheduler ───────────────────────────────────────
scheduler = BackgroundScheduler()
scheduler.add_job(_actualizar_tc, "interval", minutes=TC_INTERVAL, id="tc_update")
scheduler.start()
_actualizar_tc()  # primera ejecución inmediata


# ─── Endpoints ───────────────────────────────────────
@app.get("/tipo-cambio")
def get_tipo_cambio():
    with _lock:
        data = {
            "tipo_cambio": float(_tc_actual["tipo_cambio"]),
            "base": TC_BASE,
            "variacion": float(_tc_actual["variacion"]),
            "timestamp": _tc_actual["timestamp"],
            "intervalo_min": TC_INTERVAL,
            "precision": 4,
        }
    data["hmac"] = _generar_hmac(data)
    return data


@app.get("/tipo-cambio/verificar")
def verificar_tc(tipo_cambio: float, timestamp: str, hmac_firma: str):
    """Verifica que un tipo de cambio no fue alterado."""
    expected = hmac.new(HMAC_KEY.encode(),
                        f"{tipo_cambio}|{timestamp}".encode(),
                        hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, hmac_firma):
        raise HTTPException(403, "Firma HMAC inválida — tipo de cambio manipulado")
    return {"valido": True, "tipo_cambio": tipo_cambio, "timestamp": timestamp}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)
