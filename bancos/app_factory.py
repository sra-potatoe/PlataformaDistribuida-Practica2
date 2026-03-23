"""
bancos/app_factory.py
Fábrica de aplicaciones FastAPI para bancos.
Crea una app configurada dado un banco_id — evita duplicar código en 9 bancos.

Uso (en cada banco_XX/app.py):
    from bancos.app_factory import crear_app_banco
    app = crear_app_banco(banco_id=1)
"""

import json
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy import text

from bancos.db_factory import get_session
from bancos.auth_jwt import verificar_jwt, verificar_anti_replay
from bancos.audit import registrar_audit
from bancos.models_pydantic import (
    CuentaResponse, BancoInfoResponse,
    VerificarRequest, VerificarResponse,
)
from config.settings import BANCOS_CONFIG


def crear_app_banco(banco_id: int) -> FastAPI:
    """
    Crea y retorna una app FastAPI completa para el banco indicado.
    Incluye: GET /info, GET /cuentas, GET /cuentas/{id}, POST /verificar.
    """
    cfg = BANCOS_CONFIG[banco_id]
    motor = cfg["motor"]
    db_name = cfg["db"]

    app = FastAPI(
        title=f"API {cfg['nombre']}",
        description=f"Banco #{banco_id} — Algoritmo: {cfg['algoritmo']}",
        version="1.0.0",
    )

    # ─── Middleware de auditoría ──────────────────────
    @app.middleware("http")
    async def audit_middleware(request: Request, call_next):
        response = await call_next(request)
        try:
            session = get_session(motor, db_name)
            registrar_audit(
                session,
                accion="API_ACCESS",
                tabla="api",
                registro_id=0,
                banco_id=banco_id,
                usuario=request.headers.get("X-User", "anonymous"),
                detalle_despues={
                    "method": request.method,
                    "path": str(request.url.path),
                    "status": response.status_code,
                },
                ip_origen=request.client.host if request.client else "unknown",
            )
            session.commit()
            session.close()
        except Exception:
            pass  # No bloquear la respuesta por error de auditoría
        return response

    # ─── GET /info ───────────────────────────────────
    @app.get("/info", response_model=BancoInfoResponse)
    def get_info():
        session = get_session(motor, db_name)
        try:
            result = session.execute(
                text("SELECT COUNT(*) FROM cuentas WHERE banco_id = :bid"),
                {"bid": banco_id},
            )
            total = result.scalar() or 0
            return BancoInfoResponse(
                banco_id=banco_id,
                nombre=cfg["nombre"],
                algoritmo_encriptacion=cfg["algoritmo"],
                total_cuentas=total,
            )
        finally:
            session.close()

    # ─── GET /cuentas ────────────────────────────────
    @app.get("/cuentas", response_model=list[CuentaResponse],
             dependencies=[Depends(verificar_jwt), Depends(verificar_anti_replay)])
    def get_cuentas(limit: int = 1000, offset: int = 0):
        session = get_session(motor, db_name)
        try:
            result = session.execute(
                text("""
                    SELECT cuenta_id, banco_id, nro_cuenta,
                           identificacion_enc, nombres_enc, apellidos_enc,
                           saldo_enc, saldo_usd, saldo_bs,
                           tipo_cambio_aplicado, codigo_verificacion,
                           estado, created_at
                    FROM cuentas
                    WHERE banco_id = :bid AND deleted_at IS NULL
                    ORDER BY cuenta_id
                    LIMIT :lim OFFSET :off
                """),
                {"bid": banco_id, "lim": limit, "off": offset},
            )
            rows = result.fetchall()
            return [
                CuentaResponse(
                    cuenta_id=r[0], banco_id=r[1], nro_cuenta=r[2],
                    identificacion_enc=r[3], nombres_enc=r[4],
                    apellidos_enc=r[5], saldo_enc=r[6],
                    saldo_usd=float(r[7] or 0), saldo_bs=float(r[8] or 0),
                    tipo_cambio_aplicado=float(r[9]) if r[9] else None,
                    codigo_verificacion=r[10], estado=r[11],
                    created_at=r[12],
                )
                for r in rows
            ]
        finally:
            session.close()

    # ─── GET /cuentas/{cuenta_id} ────────────────────
    @app.get("/cuentas/{cuenta_id}", response_model=CuentaResponse,
             dependencies=[Depends(verificar_jwt), Depends(verificar_anti_replay)])
    def get_cuenta(cuenta_id: int):
        session = get_session(motor, db_name)
        try:
            result = session.execute(
                text("""
                    SELECT cuenta_id, banco_id, nro_cuenta,
                           identificacion_enc, nombres_enc, apellidos_enc,
                           saldo_enc, saldo_usd, saldo_bs,
                           tipo_cambio_aplicado, codigo_verificacion,
                           estado, created_at
                    FROM cuentas
                    WHERE cuenta_id = :cid AND banco_id = :bid AND deleted_at IS NULL
                """),
                {"cid": cuenta_id, "bid": banco_id},
            )
            r = result.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Cuenta no encontrada")
            return CuentaResponse(
                cuenta_id=r[0], banco_id=r[1], nro_cuenta=r[2],
                identificacion_enc=r[3], nombres_enc=r[4],
                apellidos_enc=r[5], saldo_enc=r[6],
                saldo_usd=float(r[7] or 0), saldo_bs=float(r[8] or 0),
                tipo_cambio_aplicado=float(r[9]) if r[9] else None,
                codigo_verificacion=r[10], estado=r[11],
                created_at=r[12],
            )
        finally:
            session.close()

    # ─── POST /verificar ─────────────────────────────
    @app.post("/verificar", response_model=VerificarResponse,
              dependencies=[Depends(verificar_jwt)])
    def verificar(data: VerificarRequest, request: Request):
        session = get_session(motor, db_name)
        try:
            # Obtener estado anterior para auditoría
            prev = session.execute(
                text("SELECT saldo_bs, estado, codigo_verificacion FROM cuentas WHERE cuenta_id = :cid"),
                {"cid": data.cuenta_id},
            ).fetchone()

            if not prev:
                raise HTTPException(404, "Cuenta no encontrada")

            # UPDATE
            session.execute(
                text("""
                    UPDATE cuentas SET
                        saldo_bs = :saldo_bs,
                        tipo_cambio_aplicado = :tc,
                        codigo_verificacion = :codigo,
                        estado = 'convertido',
                        updated_at = :now,
                        updated_by = :user
                    WHERE cuenta_id = :cid
                """),
                {
                    "saldo_bs": data.saldo_bs,
                    "tc": data.tipo_cambio_aplicado,
                    "codigo": data.codigo_verificacion,
                    "now": datetime.now(timezone.utc),
                    "user": data.updated_by,
                    "cid": data.cuenta_id,
                },
            )

            # Auditoría
            registrar_audit(
                session,
                accion="CONVERSION",
                tabla="cuentas",
                registro_id=data.cuenta_id,
                banco_id=banco_id,
                usuario=data.updated_by,
                detalle_antes={
                    "saldo_bs": float(prev[0] or 0),
                    "estado": prev[1],
                    "codigo": prev[2],
                },
                detalle_despues={
                    "saldo_bs": data.saldo_bs,
                    "tipo_cambio": data.tipo_cambio_aplicado,
                    "codigo": data.codigo_verificacion,
                    "estado": "convertido",
                },
                ip_origen=request.client.host if request.client else "unknown",
            )

            session.commit()

            return VerificarResponse(
                cuenta_id=data.cuenta_id,
                codigo_verificacion=data.codigo_verificacion,
                estado="convertido",
                mensaje="Saldo actualizado correctamente",
            )
        except HTTPException:
            raise
        except Exception as e:
            session.rollback()
            raise HTTPException(500, f"Error al verificar: {e}")
        finally:
            session.close()

    return app
