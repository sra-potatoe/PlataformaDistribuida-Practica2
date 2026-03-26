-- schema_asfi.sql — BD Central ASFI (PostgreSQL)
CREATE TABLE IF NOT EXISTS bancos (
    banco_id INT PRIMARY KEY, nombre VARCHAR(100), algoritmo VARCHAR(50)
);
CREATE TABLE IF NOT EXISTS cuentas_asfi (
    cuenta_id BIGINT PRIMARY KEY,
    banco_id INT REFERENCES bancos(banco_id),
    nro_cuenta VARCHAR(20), nombre_cliente VARCHAR(200), ci VARCHAR(20),
    saldo_usd DECIMAL(18,4), saldo_bs DECIMAL(18,4),
    tipo_cambio DECIMAL(10,4), fecha_conversion TIMESTAMP,
    codigo_verificacion CHAR(8), estado VARCHAR(20) DEFAULT 'pendiente'
);
CREATE TABLE IF NOT EXISTS log_auditoria (
    id BIGSERIAL PRIMARY KEY,
    timestamp_op TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_cambio DECIMAL(10,4), cuenta_id BIGINT, banco_id INT,
    accion VARCHAR(50), detalle TEXT
);
INSERT INTO bancos VALUES
(1,'Banco Unión S.A.','cesar'),(2,'Banco Mercantil Santa Cruz S.A.','atbash'),
(3,'Banco Nacional de Bolivia S.A.','vigenere'),(4,'Banco de Crédito de Bolivia S.A.','playfair'),
(5,'Banco BISA S.A.','hill'),(6,'Banco Ganadero S.A.','des'),
(7,'Banco Económico S.A.','3des'),(8,'Banco Prodem S.A.','blowfish'),
(9,'Banco Solidario S.A.','twofish'),(10,'Banco Fortaleza S.A.','aes'),
(11,'Banco FIE S.A.','rsa'),(12,'Banco PYME de la Comunidad S.A.','elgamal'),
(13,'Banco de Desarrollo Productivo S.A.M.','ecc'),(14,'Banco de la Nación Argentina','chacha20')
ON CONFLICT (banco_id) DO NOTHING;
