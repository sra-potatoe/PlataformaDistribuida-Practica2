"""
asfi/services/verificacion.py — Genera código de verificación y envía a bancos.
Uso: from asfi.services.verificacion import generar_codigo, enviar_verificacion
"""
import secrets, uuid, time
import httpx
from bancos.auth_jwt import crear_token

def generar_codigo() -> str:
    """8 chars hex: 0-9 A-F (ej: A3F2B1C9)."""
    return secrets.token_hex(4).upper()

def enviar_verificacion(banco_url: str, banco_id: int, cuenta_id: int,
                         saldo_bs: float, tipo_cambio: float) -> dict:
    codigo = generar_codigo()
    payload = {"cuenta_id": cuenta_id, "codigo_verificacion": codigo,
               "saldo_bs": round(saldo_bs, 4), "tipo_cambio_aplicado": round(tipo_cambio, 4)}
    headers = {"Authorization": f"Bearer {crear_token(banco_id)}",
               "X-Nonce": str(uuid.uuid4()), "X-Timestamp": str(time.time())}
    try:
        with httpx.Client(verify=False, timeout=15) as c:
            r = c.post(f"{banco_url}/verificar", json=payload, headers=headers)
            return {"cuenta_id": cuenta_id, "codigo": codigo, "status": r.status_code,
                    "response": r.json() if r.status_code == 200 else r.text}
    except Exception as e:
        return {"cuenta_id": cuenta_id, "codigo": codigo, "status": -1, "error": str(e)}
