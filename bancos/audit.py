"""
bancos/audit.py
Helper para insertar registros de auditoría en cualquier BD relacional.
"""

import json
from datetime import datetime, timezone
from sqlalchemy import text


def registrar_audit(session, accion: str, tabla: str, registro_id: int,
                    banco_id: int, usuario: str = "SYSTEM",
                    detalle_antes: dict = None, detalle_despues: dict = None,
                    ip_origen: str = "127.0.0.1"):
    """
    Inserta un registro en audit_log.

    Args:
        session: SQLAlchemy session
        accion: INSERT | UPDATE | DELETE | CONVERSION | LOGIN | API_ACCESS
        tabla: nombre de la tabla afectada (e.g. 'cuentas')
        registro_id: ID del registro afectado
        banco_id: ID del banco
        usuario: quién hizo la acción
        detalle_antes: estado anterior (para UPDATE/DELETE)
        detalle_despues: estado posterior (para INSERT/UPDATE)
        ip_origen: IP del cliente
    """
    antes_json = json.dumps(detalle_antes, ensure_ascii=False, default=str) if detalle_antes else None
    despues_json = json.dumps(detalle_despues, ensure_ascii=False, default=str) if detalle_despues else None

    session.execute(
        text("""
            INSERT INTO audit_log (accion, tabla_afectada, registro_id, banco_id,
                                   usuario, detalle_antes, detalle_despues, ip_origen)
            VALUES (:accion, :tabla, :registro_id, :banco_id,
                    :usuario, :antes, :despues, :ip)
        """),
        {
            "accion": accion,
            "tabla": tabla,
            "registro_id": registro_id,
            "banco_id": banco_id,
            "usuario": usuario,
            "antes": antes_json,
            "despues": despues_json,
            "ip": ip_origen,
        }
    )


def registrar_audit_firebase(db_ref, accion: str, registro_id: int,
                              banco_id: int, usuario: str = "SYSTEM",
                              detalle_antes: dict = None,
                              detalle_despues: dict = None,
                              ip_origen: str = "127.0.0.1"):
    """
    Inserta un registro de auditoría en Firestore.

    Args:
        db_ref: referencia Firestore (colección audit_log del banco)
        Otros args: iguales a registrar_audit()
    """
    doc = {
        "timestamp_op": datetime.now(timezone.utc),
        "accion": accion,
        "registro_id": registro_id,
        "banco_id": banco_id,
        "usuario": usuario,
        "detalle_antes": detalle_antes,
        "detalle_despues": detalle_despues,
        "ip_origen": ip_origen,
    }
    db_ref.add(doc)
