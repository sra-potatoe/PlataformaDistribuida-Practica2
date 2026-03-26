"""
scripts/validar_consistencia.py — Compara saldo en BD banco vs BD ASFI.
Genera reporte de inconsistencias.

Uso: python -m scripts.validar_consistencia
"""
import sys, os, json
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text, create_engine
from config.settings import (BANCOS, ASFI_HOST, ASFI_PORT, ASFI_USER, ASFI_PASS, ASFI_DB)
from bancos.db_factory import get_session

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_asfi_session():
    url = f"postgresql+psycopg2://{ASFI_USER}:{ASFI_PASS}@{ASFI_HOST}:{ASFI_PORT}/{ASFI_DB}"
    from sqlalchemy.orm import sessionmaker
    eng = create_engine(url)
    return sessionmaker(bind=eng)()


def main():
    print("=" * 60)
    print("  VALIDACIÓN DE CONSISTENCIA — Banco vs ASFI")
    print("=" * 60)

    asfi = get_asfi_session()
    inconsistencias = []

    for bid, cfg in BANCOS.items():
        if cfg["motor"] in ("mongo", "fire"):
            print(f"  Banco {bid:2d} ({cfg['nombre'][:20]:20s}): skip (NoSQL)")
            continue
        try:
            banco_s = get_session(cfg["motor"], cfg["db"])

            # Contar en banco
            n_banco = banco_s.execute(
                text("SELECT COUNT(*) FROM cuentas WHERE banco_id=:b"), {"b": bid}
            ).scalar() or 0

            # Contar en ASFI
            n_asfi = asfi.execute(
                text("SELECT COUNT(*) FROM cuentas_asfi WHERE banco_id=:b"), {"b": bid}
            ).scalar() or 0

            # Comparar saldos convertidos
            sum_banco = banco_s.execute(
                text("SELECT COALESCE(SUM(saldo_bs),0) FROM cuentas WHERE banco_id=:b AND estado='convertido'"),
                {"b": bid}
            ).scalar() or 0

            sum_asfi = asfi.execute(
                text("SELECT COALESCE(SUM(saldo_bs),0) FROM cuentas_asfi WHERE banco_id=:b"),
                {"b": bid}
            ).scalar() or 0

            diff = abs(float(sum_banco) - float(sum_asfi))
            ok = "✓" if n_banco == n_asfi and diff < 0.01 else "✗"

            print(f"  {ok} Banco {bid:2d}: cuentas={n_banco}/{n_asfi}  saldo_bs={float(sum_banco):.2f}/{float(sum_asfi):.2f}  diff={diff:.4f}")

            if n_banco != n_asfi or diff >= 0.01:
                inconsistencias.append({
                    "banco_id": bid, "nombre": cfg["nombre"],
                    "cuentas_banco": n_banco, "cuentas_asfi": n_asfi,
                    "saldo_bs_banco": float(sum_banco), "saldo_bs_asfi": float(sum_asfi),
                    "diferencia": diff,
                })

            banco_s.close()
        except Exception as e:
            print(f"  ✗ Banco {bid:2d}: ERROR — {e}")
            inconsistencias.append({"banco_id": bid, "error": str(e)})

    asfi.close()

    # Guardar reporte
    report_path = os.path.join(BASE, "logs", "reporte_consistencia.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_inconsistencias": len(inconsistencias),
            "detalle": inconsistencias,
        }, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    if inconsistencias:
        print(f"  ⚠ {len(inconsistencias)} inconsistencias encontradas")
    else:
        print("  ✓ Sin inconsistencias — todo consistente")
    print(f"  Reporte: {report_path}")


if __name__ == "__main__":
    main()
