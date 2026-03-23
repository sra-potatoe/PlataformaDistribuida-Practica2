-- ============================================================
-- schema_mysql.sql
-- MySQL — Bancos: Económico (7), Prodem (8), Solidario (9)
-- Ejecutar en cada BD: banco_economico, banco_prodem, banco_solidario
-- ============================================================

CREATE TABLE IF NOT EXISTS bancos (
    banco_id                INT PRIMARY KEY,
    nombre                  VARCHAR(100) NOT NULL,
    algoritmo_encriptacion  VARCHAR(50) NOT NULL,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by              VARCHAR(50) DEFAULT 'SYSTEM',
    updated_at              TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    updated_by              VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS cuentas (
    cuenta_id               BIGINT AUTO_INCREMENT PRIMARY KEY,
    banco_id                INT NOT NULL,
    nro_cuenta              VARCHAR(20) NOT NULL,
    identificacion_enc      TEXT NOT NULL,
    nombres_enc             TEXT NOT NULL,
    apellidos_enc           TEXT NOT NULL,
    saldo_enc               TEXT NOT NULL,
    saldo_usd               DECIMAL(18,4) DEFAULT 0.0000,
    saldo_bs                DECIMAL(18,4) DEFAULT 0.0000,
    tipo_cambio_aplicado    DECIMAL(10,4),
    codigo_verificacion     CHAR(8),
    estado                  VARCHAR(20) DEFAULT 'pendiente',
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by              VARCHAR(50) DEFAULT 'SYSTEM',
    updated_at              TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    updated_by              VARCHAR(50),
    deleted_at              TIMESTAMP NULL,
    deleted_by              VARCHAR(50),
    FOREIGN KEY (banco_id) REFERENCES bancos(banco_id),
    INDEX idx_banco_id (banco_id),
    INDEX idx_estado (estado),
    INDEX idx_nro_cuenta (nro_cuenta)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS audit_log (
    log_id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp_op    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accion          VARCHAR(20) NOT NULL,
    tabla_afectada  VARCHAR(50) NOT NULL,
    registro_id     BIGINT,
    banco_id        INT,
    usuario         VARCHAR(50),
    detalle_antes   TEXT,
    detalle_despues TEXT,
    ip_origen       VARCHAR(45),
    INDEX idx_banco (banco_id),
    INDEX idx_accion (accion),
    INDEX idx_timestamp (timestamp_op)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
