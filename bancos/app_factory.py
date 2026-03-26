"""bancos/app_factory.py — Crea una FastAPI app para cualquier banco."""
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy import text
from bancos.db_factory import get_session
from bancos.auth_jwt import verificar_jwt, verificar_replay
from bancos.audit import audit_sql
from bancos.models_pydantic import CuentaOut, BancoInfo, VerificarIn, VerificarOut
from config.settings import BANCOS

def crear_app(bid: int) -> FastAPI:
    cfg = BANCOS[bid]
    m, db = cfg["motor"], cfg["db"]
    app = FastAPI(title=f"API {cfg['nombre']}", version="1.0.0")

    @app.middleware("http")
    async def audit_mw(req: Request, call_next):
        resp = await call_next(req)
        try:
            s = get_session(m, db)
            audit_sql(s, "API_ACCESS", "api", 0, bid,
                      despues={"method": req.method, "path": str(req.url.path), "status": resp.status_code},
                      ip=req.client.host if req.client else "?")
            s.commit(); s.close()
        except Exception: pass
        return resp

    @app.get("/info", response_model=BancoInfo)
    def info():
        s = get_session(m, db)
        n = s.execute(text("SELECT COUNT(*) FROM cuentas WHERE banco_id=:b"), {"b": bid}).scalar() or 0
        s.close()
        return BancoInfo(banco_id=bid, nombre=cfg["nombre"], algoritmo=cfg["algo"], total_cuentas=n)

    @app.get("/cuentas", response_model=list[CuentaOut],
             dependencies=[Depends(verificar_jwt), Depends(verificar_replay)])
    def listar(limit: int = 1000, offset: int = 0):
        s = get_session(m, db)
        rows = s.execute(text(
            "SELECT cuenta_id,banco_id,nro_cuenta,identificacion_enc,nombres_enc,"
            "apellidos_enc,saldo_enc,saldo_usd,saldo_bs,tipo_cambio_aplicado,"
            "codigo_verificacion,estado,created_at FROM cuentas "
            "WHERE banco_id=:b AND deleted_at IS NULL ORDER BY cuenta_id LIMIT :l OFFSET :o"),
            {"b": bid, "l": limit, "o": offset}).fetchall()
        s.close()
        return [CuentaOut(cuenta_id=r[0],banco_id=r[1],nro_cuenta=r[2],
                          identificacion_enc=r[3],nombres_enc=r[4],apellidos_enc=r[5],
                          saldo_enc=r[6],saldo_usd=float(r[7] or 0),saldo_bs=float(r[8] or 0),
                          tipo_cambio_aplicado=float(r[9]) if r[9] else None,
                          codigo_verificacion=r[10],estado=r[11],created_at=r[12]) for r in rows]

    @app.get("/cuentas/{cid}", response_model=CuentaOut,
             dependencies=[Depends(verificar_jwt), Depends(verificar_replay)])
    def detalle(cid: int):
        s = get_session(m, db)
        r = s.execute(text(
            "SELECT cuenta_id,banco_id,nro_cuenta,identificacion_enc,nombres_enc,"
            "apellidos_enc,saldo_enc,saldo_usd,saldo_bs,tipo_cambio_aplicado,"
            "codigo_verificacion,estado,created_at FROM cuentas WHERE cuenta_id=:c AND banco_id=:b"),
            {"c": cid, "b": bid}).fetchone()
        s.close()
        if not r: raise HTTPException(404, "Cuenta no encontrada")
        return CuentaOut(cuenta_id=r[0],banco_id=r[1],nro_cuenta=r[2],
                         identificacion_enc=r[3],nombres_enc=r[4],apellidos_enc=r[5],
                         saldo_enc=r[6],saldo_usd=float(r[7] or 0),saldo_bs=float(r[8] or 0),
                         tipo_cambio_aplicado=float(r[9]) if r[9] else None,
                         codigo_verificacion=r[10],estado=r[11],created_at=r[12])

    @app.post("/verificar", response_model=VerificarOut, dependencies=[Depends(verificar_jwt)])
    def verificar(data: VerificarIn, req: Request):
        s = get_session(m, db)
        prev = s.execute(text("SELECT saldo_bs,estado,codigo_verificacion FROM cuentas WHERE cuenta_id=:c"),
                         {"c": data.cuenta_id}).fetchone()
        if not prev: raise HTTPException(404, "Cuenta no encontrada")
        s.execute(text(
            "UPDATE cuentas SET saldo_bs=:sb,tipo_cambio_aplicado=:tc,codigo_verificacion=:cd,"
            "estado='convertido',updated_at=:now,updated_by=:u WHERE cuenta_id=:c"),
            {"sb": data.saldo_bs, "tc": data.tipo_cambio_aplicado, "cd": data.codigo_verificacion,
             "now": datetime.now(timezone.utc), "u": data.updated_by, "c": data.cuenta_id})
        audit_sql(s, "CONVERSION", "cuentas", data.cuenta_id, bid, data.updated_by,
                  antes={"saldo_bs": float(prev[0] or 0), "estado": prev[1]},
                  despues={"saldo_bs": data.saldo_bs, "codigo": data.codigo_verificacion},
                  ip=req.client.host if req.client else "?")
        s.commit(); s.close()
        return VerificarOut(cuenta_id=data.cuenta_id, codigo_verificacion=data.codigo_verificacion,
                            estado="convertido", mensaje="Saldo actualizado")
    return app
