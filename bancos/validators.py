"""bancos/validators.py — Validaciones de filas del CSV."""

def validar_fila(f: dict) -> tuple[bool, str]:
    """Retorna (es_valida, motivo_rechazo)."""
    for campo in ("Identificacion", "Nombres", "Apellidos", "NroCuenta"):
        val = f.get(campo, "")
        if not val or not str(val).strip():
            return False, f"sin {campo}"
    if not f.get("IdBanco"):
        return False, "sin banco"
    if f.get("Saldo") is None or f.get("Saldo") == "":
        return False, "sin saldo"
    return True, ""

def estado_por_saldo(saldo: float) -> str:
    if saldo < 0:       return "saldo_negativo"
    if saldo < 0.0001:  return "saldo_minimo"
    return "pendiente"
