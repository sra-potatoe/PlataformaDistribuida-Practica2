"""
bancos/auth_jwt.py
Autenticación JWT compartida por todas las APIs de bancos.
"""

import time
import uuid
from datetime import datetime, timedelta, timezone
from fastapi import Header, HTTPException
from jose import JWTError, jwt
from config.settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

# Cache de nonces usados (anti-replay)
_used_nonces: set = set()


def crear_token(banco_id: int, subject: str = "asfi") -> str:
    """Genera un JWT firmado. Usado por ASFI para autenticarse contra los bancos."""
    payload = {
        "sub": subject,
        "banco_id": banco_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def verificar_jwt(authorization: str = Header(..., alias="Authorization")) -> dict:
    """
    Dependency de FastAPI: valida el JWT del header Authorization.
    Retorna el payload decodificado.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato: Bearer <token>")

    token = authorization[7:]  # quitar "Bearer "
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")

    return payload


def verificar_anti_replay(
    x_nonce: str = Header(...),
    x_timestamp: str = Header(...),
) -> None:
    """
    Dependency de FastAPI: previene ataques de replay.
    - Rechaza si el timestamp tiene más de 60 segundos de diferencia.
    - Rechaza si el nonce ya fue usado.
    """
    # Validar timestamp
    try:
        ts = float(x_timestamp)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="X-Timestamp inválido")

    if abs(time.time() - ts) > 60:
        raise HTTPException(status_code=403, detail="Timestamp expirado (>60s)")

    # Validar nonce único
    if x_nonce in _used_nonces:
        raise HTTPException(status_code=403, detail="Nonce ya utilizado (replay)")

    _used_nonces.add(x_nonce)

    # Limpiar nonces viejos (cada 1000 entradas)
    if len(_used_nonces) > 10000:
        _used_nonces.clear()
