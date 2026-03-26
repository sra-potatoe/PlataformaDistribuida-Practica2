"""bancos/auth_jwt.py — JWT + anti-replay para APIs."""
import time, uuid
from datetime import datetime, timedelta, timezone
from fastapi import Header, HTTPException
from jose import JWTError, jwt
from config.settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MIN

_used_nonces: set = set()

def crear_token(banco_id: int, sub: str = "asfi") -> str:
    payload = {"sub": sub, "banco_id": banco_id,
               "iat": datetime.now(timezone.utc),
               "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MIN),
               "jti": str(uuid.uuid4())}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verificar_jwt(authorization: str = Header(..., alias="Authorization")) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Formato: Bearer <token>")
    try:
        return jwt.decode(authorization[7:], JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise HTTPException(401, f"Token inválido: {e}")

def verificar_replay(x_nonce: str = Header(...), x_timestamp: str = Header(...)):
    try:
        ts = float(x_timestamp)
    except (ValueError, TypeError):
        raise HTTPException(400, "X-Timestamp inválido")
    if abs(time.time() - ts) > 60:
        raise HTTPException(403, "Timestamp expirado")
    if x_nonce in _used_nonces:
        raise HTTPException(403, "Nonce reutilizado (replay)")
    _used_nonces.add(x_nonce)
    if len(_used_nonces) > 10000:
        _used_nonces.clear()
