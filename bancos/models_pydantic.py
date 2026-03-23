"""
bancos/models_pydantic.py
Modelos Pydantic compartidos por todas las APIs de bancos.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CuentaResponse(BaseModel):
    """Respuesta de GET /cuentas — datos cifrados."""
    cuenta_id: int
    banco_id: int
    nro_cuenta: str
    identificacion_enc: str
    nombres_enc: str
    apellidos_enc: str
    saldo_enc: str
    saldo_usd: float
    saldo_bs: float
    tipo_cambio_aplicado: Optional[float] = None
    codigo_verificacion: Optional[str] = None
    estado: str
    created_at: Optional[datetime] = None


class BancoInfoResponse(BaseModel):
    """Respuesta de GET /info."""
    banco_id: int
    nombre: str
    algoritmo_encriptacion: str
    total_cuentas: int


class VerificarRequest(BaseModel):
    """Body de POST /verificar."""
    cuenta_id: int
    codigo_verificacion: str
    saldo_bs: float
    tipo_cambio_aplicado: float
    updated_by: str = "ASFI"


class VerificarResponse(BaseModel):
    """Respuesta de POST /verificar."""
    cuenta_id: int
    codigo_verificacion: str
    estado: str
    mensaje: str
