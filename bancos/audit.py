"""bancos/audit.py — Helpers de auditoría para SQL y Firebase."""
import json
from datetime import datetime, timezone
from sqlalchemy import text

def audit_sql(session, accion, tabla, reg_id, banco_id, usuario="SYSTEM",
              antes=None, despues=None, ip="127.0.0.1"):
    a = json.dumps(antes, ensure_ascii=False, default=str) if antes else None
    d = json.dumps(despues, ensure_ascii=False, default=str) if despues else None
    session.execute(text(
        "INSERT INTO audit_log(accion,tabla,registro_id,banco_id,usuario,antes,despues,ip) "
        "VALUES(:a,:t,:r,:b,:u,:an,:de,:ip)"),
        {"a": accion, "t": tabla, "r": reg_id, "b": banco_id,
         "u": usuario, "an": a, "de": d, "ip": ip})

def audit_fire(col_ref, accion, reg_id, banco_id, usuario="SYSTEM",
               antes=None, despues=None, ip="127.0.0.1"):
    col_ref.add({"timestamp_op": datetime.now(timezone.utc), "accion": accion,
                 "registro_id": reg_id, "banco_id": banco_id, "usuario": usuario,
                 "antes": antes, "despues": despues, "ip": ip})
