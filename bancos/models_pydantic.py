"""bancos/models_pydantic.py — Schemas compartidos para APIs."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CuentaOut(BaseModel):
    cuenta_id: int; banco_id: int; nro_cuenta: str
    identificacion_enc: str; nombres_enc: str; apellidos_enc: str; saldo_enc: str
    saldo_usd: float; saldo_bs: float
    tipo_cambio_aplicado: Optional[float] = None
    codigo_verificacion: Optional[str] = None
    estado: str; created_at: Optional[datetime] = None

class BancoInfo(BaseModel):
    banco_id: int; nombre: str; algoritmo: str; total_cuentas: int

class VerificarIn(BaseModel):
    cuenta_id: int; codigo_verificacion: str; saldo_bs: float
    tipo_cambio_aplicado: float; updated_by: str = "ASFI"

class VerificarOut(BaseModel):
    cuenta_id: int; codigo_verificacion: str; estado: str; mensaje: str
