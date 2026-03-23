-- ============================================================
-- schema_sqlserver.sql
-- SQL Server — Bancos: BCP (4), BISA (5), Ganadero (6)
-- Ejecutar en cada BD: banco_bcp, banco_bisa, banco_ganadero
-- ============================================================

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'bancos')
CREATE TABLE bancos (
    banco_id                INT PRIMARY KEY,
    nombre                  NVARCHAR(100) NOT NULL,
    algoritmo_encriptacion  NVARCHAR(50) NOT NULL,
    created_at              DATETIME2 DEFAULT GETDATE(),
    created_by              NVARCHAR(50) DEFAULT 'SYSTEM',
    updated_at              DATETIME2,
    updated_by              NVARCHAR(50)
);
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'cuentas')
CREATE TABLE cuentas (
    cuenta_id               BIGINT IDENTITY(1,1) PRIMARY KEY,
    banco_id                INT NOT NULL FOREIGN KEY REFERENCES bancos(banco_id),
    nro_cuenta              NVARCHAR(20) NOT NULL,
    identificacion_enc      NVARCHAR(MAX) NOT NULL,
    nombres_enc             NVARCHAR(MAX) NOT NULL,
    apellidos_enc           NVARCHAR(MAX) NOT NULL,
    saldo_enc               NVARCHAR(MAX) NOT NULL,
    saldo_usd               DECIMAL(18,4) DEFAULT 0.0000,
    saldo_bs                DECIMAL(18,4) DEFAULT 0.0000,
    tipo_cambio_aplicado    DECIMAL(10,4),
    codigo_verificacion     CHAR(8),
    estado                  NVARCHAR(20) DEFAULT 'pendiente',
    created_at              DATETIME2 DEFAULT GETDATE(),
    created_by              NVARCHAR(50) DEFAULT 'SYSTEM',
    updated_at              DATETIME2,
    updated_by              NVARCHAR(50),
    deleted_at              DATETIME2,
    deleted_by              NVARCHAR(50)
);
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'audit_log')
CREATE TABLE audit_log (
    log_id          BIGINT IDENTITY(1,1) PRIMARY KEY,
    timestamp_op    DATETIME2 DEFAULT GETDATE(),
    accion          NVARCHAR(20) NOT NULL,
    tabla_afectada  NVARCHAR(50) NOT NULL,
    registro_id     BIGINT,
    banco_id        INT,
    usuario         NVARCHAR(50),
    detalle_antes   NVARCHAR(MAX),
    detalle_despues NVARCHAR(MAX),
    ip_origen       NVARCHAR(45)
);
GO

-- Índices
CREATE INDEX idx_cuentas_banco_id ON cuentas(banco_id);
CREATE INDEX idx_cuentas_estado ON cuentas(estado);
CREATE INDEX idx_cuentas_nro_cuenta ON cuentas(nro_cuenta);
CREATE INDEX idx_audit_log_banco ON audit_log(banco_id);
CREATE INDEX idx_audit_log_accion ON audit_log(accion);
GO
