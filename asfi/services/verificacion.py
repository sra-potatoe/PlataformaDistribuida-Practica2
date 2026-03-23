"""
asfi/services/verificacion.py
Genera código de verificación y envía a los bancos.

Uso:
    from asfi.services.verificacion import generar_codigo, enviar_verificacion
"""

import secrets
import uuid
import time

import httpx
from bancos.auth_jwt import crear_token


def generar_codigo() -> str:
    """Genera un código de verificación de 8 caracteres hexadecimales (0-9, A-F)."""
    return secrets.token_hex(4).upper()


def enviar_verificacion(
    banco_url: str,
    banco_id: int,
    cuenta_id: int,
    saldo_bs: float,
    tipo_cambio: float,
) -> dict:
    """
    Envía el código de verificación al banco vía POST /verificar.

    Args:
        banco_url: URL base de la API del banco (e.g. "https://localhost:8001")
        banco_id: ID del banco
        cuenta_id: ID de la cuenta
        saldo_bs: Saldo convertido en Bs.
        tipo_cambio: Tipo de cambio aplicado

    Returns:
        dict con: codigo, status, response
    """
    codigo = generar_codigo()
    token = crear_token(banco_id)

    payload = {
        "cuenta_id": cuenta_id,
        "codigo_verificacion": codigo,
        "saldo_bs": round(saldo_bs, 4),
        "tipo_cambio_aplicado": round(tipo_cambio, 4),
        "updated_by": "ASFI",
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Nonce": str(uuid.uuid4()),
        "X-Timestamp": str(time.time()),
        "Content-Type": "application/json",
    }

    try:
        with httpx.Client(verify=False, timeout=15.0) as client:
            resp = client.post(f"{banco_url}/verificar", json=payload, headers=headers)
            return {
                "cuenta_id": cuenta_id,
                "codigo": codigo,
                "status": resp.status_code,
                "response": resp.json() if resp.status_code == 200 else resp.text,
            }
    except Exception as e:
        return {
            "cuenta_id": cuenta_id,
            "codigo": codigo,
            "status": -1,
            "error": str(e),
        }
