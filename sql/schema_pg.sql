-- schema_pg.sql — PostgreSQL (Unión, Mercantil, BNB)
CREATE TABLE IF NOT EXISTS bancos (
    banco_id                INT PRIMARY KEY,
    nombre                  VARCHAR(100) NOT NULL,
    algoritmo_encriptacion  VARCHAR(50) NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by  VARCHAR(50) DEFAULT 'SYSTEM',
    updated_at  TIMESTAMP, updated_by VARCHAR(50)
);
CREATE TABLE IF NOT EXISTS cuentas (
    cuenta_id            BIGSERIAL PRIMARY KEY,
    banco_id             INT NOT NULL REFERENCES bancos(banco_id),
    nro_cuenta           VARCHAR(20) NOT NULL,
    identificacion_enc   TEXT NOT NULL,
    nombres_enc          TEXT NOT NULL,
    apellidos_enc        TEXT NOT NULL,
    saldo_enc            TEXT NOT NULL,
    saldo_usd            DECIMAL(18,4) DEFAULT 0,
    saldo_bs             DECIMAL(18,4) DEFAULT 0,
    tipo_cambio_aplicado DECIMAL(10,4),
    codigo_verificacion  CHAR(8),
    estado               VARCHAR(20) DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) DEFAULT 'SYSTEM',
    updated_at TIMESTAMP, updated_by VARCHAR(50),
    deleted_at TIMESTAMP, deleted_by VARCHAR(50)
);
CREATE TABLE IF NOT EXISTS audit_log (
    log_id       BIGSERIAL PRIMARY KEY,
    timestamp_op TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accion       VARCHAR(20) NOT NULL,
    tabla        VARCHAR(50) NOT NULL,
    registro_id  BIGINT, banco_id INT,
    usuario      VARCHAR(50),
    antes TEXT, despues TEXT, ip VARCHAR(45)
);
CREATE INDEX IF NOT EXISTS ix_cuentas_banco ON cuentas(banco_id);
CREATE INDEX IF NOT EXISTS ix_cuentas_estado ON cuentas(estado);
CREATE INDEX IF NOT EXISTS ix_audit_banco ON audit_log(banco_id);
CREATE INDEX IF NOT EXISTS ix_audit_ts ON audit_log(timestamp_op);
