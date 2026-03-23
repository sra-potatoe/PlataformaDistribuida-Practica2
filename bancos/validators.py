"""
bancos/validators.py
Validaciones de datos al poblar las BDs.
"""


def validar_fila(fila: dict) -> tuple[bool, str]:
    """
    Valida una fila del CSV antes de insertar.

    Args:
        fila: dict con claves: Identificacion, Nombres, Apellidos, NroCuenta, IdBanco, Saldo

    Returns:
        (es_valida, motivo_rechazo)
        Si es_valida=True, motivo_rechazo=""
        Si es_valida=False, motivo_rechazo="sin identificación" etc.
    """
    # --- Campos obligatorios (NO pueden faltar) ---
    identificacion = fila.get("Identificacion", "")
    if not identificacion or not str(identificacion).strip():
        return False, "sin identificación"

    nombres = fila.get("Nombres", "")
    if not nombres or not str(nombres).strip():
        return False, "sin nombres"

    apellidos = fila.get("Apellidos", "")
    if not apellidos or not str(apellidos).strip():
        return False, "sin apellidos"

    nro_cuenta = fila.get("NroCuenta", "")
    if not nro_cuenta or not str(nro_cuenta).strip():
        return False, "sin número de cuenta"

    id_banco = fila.get("IdBanco", "")
    if not id_banco:
        return False, "sin banco asignado"

    saldo = fila.get("Saldo", "")
    if saldo == "" or saldo is None:
        return False, "sin saldo"

    return True, ""


def determinar_estado(saldo: float) -> str:
    """
    Determina el estado de la cuenta según el saldo.

    - saldo < 0       → 'saldo_negativo' (se carga, NO se convierte)
    - 0 ≤ saldo < 0.0001 → 'saldo_minimo' (se carga, NO se convierte)
    - saldo ≥ 0.0001  → 'pendiente' (se aplicará conversión)
    """
    if saldo < 0:
        return "saldo_negativo"
    elif saldo < 0.0001:
        return "saldo_minimo"
    else:
        return "pendiente"
