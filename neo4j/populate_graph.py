"""
neo4j/populate_graph.py — Pobla Neo4j con nodos :Cliente y :Cuenta.
Relación (:Cliente)-[:TIENE_CUENTA]->(:Cuenta).
Lee datos de la BD central ASFI.

Uso: python -m neo4j.populate_graph
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neo4j import GraphDatabase
from sqlalchemy import text, create_engine
from config.settings import (NEO4J_URI, NEO4J_USER, NEO4J_PASS,
                              ASFI_HOST, ASFI_PORT, ASFI_USER, ASFI_PASS, ASFI_DB)


def get_asfi_engine():
    return create_engine(
        f"postgresql+psycopg2://{ASFI_USER}:{ASFI_PASS}@{ASFI_HOST}:{ASFI_PORT}/{ASFI_DB}")


def poblar_neo4j():
    engine = get_asfi_engine()
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

    with driver.session() as neo:
        # Limpiar
        neo.run("MATCH (n) DETACH DELETE n")

        # Índices
        neo.run("CREATE INDEX IF NOT EXISTS FOR (c:Cliente) ON (c.ci)")
        neo.run("CREATE INDEX IF NOT EXISTS FOR (cu:Cuenta) ON (cu.cuenta_id)")

        with engine.connect() as conn:
            rows = conn.execute(text(
                "SELECT cuenta_id, banco_id, nro_cuenta, nombre_cliente, ci, "
                "saldo_usd, saldo_bs FROM cuentas_asfi"
            )).fetchall()

        print(f"Cargando {len(rows)} registros a Neo4j...")
        batch = []
        for r in rows:
            batch.append({
                "cuenta_id": r[0], "banco_id": r[1], "nro_cuenta": r[2],
                "nombre": r[3] or "N/A", "ci": r[4] or "N/A",
                "saldo_usd": float(r[5] or 0), "saldo_bs": float(r[6] or 0),
            })
            if len(batch) >= 500:
                _insertar_batch(neo, batch)
                batch = []
        if batch:
            _insertar_batch(neo, batch)

    driver.close()
    print(f"✓ Neo4j poblado con {len(rows)} relaciones Cliente→Cuenta")


def _insertar_batch(session, batch):
    session.run("""
        UNWIND $batch AS row
        MERGE (cl:Cliente {ci: row.ci})
          ON CREATE SET cl.nombre = row.nombre
        MERGE (cu:Cuenta {cuenta_id: row.cuenta_id})
          ON CREATE SET cu.banco_id = row.banco_id,
                        cu.nro_cuenta = row.nro_cuenta,
                        cu.saldo_usd = row.saldo_usd,
                        cu.saldo_bs = row.saldo_bs
        MERGE (cl)-[:TIENE_CUENTA]->(cu)
    """, batch=batch)


if __name__ == "__main__":
    poblar_neo4j()
