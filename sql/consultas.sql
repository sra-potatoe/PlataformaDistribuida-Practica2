-- ============================================================
-- sql/consultas.sql — 8 Consultas SQL (Sin IA)
-- Ejecutar sobre la BD central ASFI (asfi_central)
-- ============================================================

-- 1) Total saldo USD por banco
SELECT b.nombre, b.algoritmo,
       COUNT(c.cuenta_id) AS total_cuentas,
       SUM(c.saldo_usd)   AS total_usd
FROM cuentas_asfi c
JOIN bancos b ON c.banco_id = b.banco_id
GROUP BY b.banco_id, b.nombre, b.algoritmo
ORDER BY total_usd DESC;

-- 2) Total saldo Bs por banco
SELECT b.nombre,
       SUM(c.saldo_bs)    AS total_bs,
       AVG(c.tipo_cambio)  AS tc_promedio
FROM cuentas_asfi c
JOIN bancos b ON c.banco_id = b.banco_id
WHERE c.estado = 'convertido'
GROUP BY b.banco_id, b.nombre
ORDER BY total_bs DESC;

-- 3) Cuenta con mayor saldo (USD y Bs)
SELECT c.cuenta_id, c.nro_cuenta, b.nombre AS banco,
       c.saldo_usd, c.saldo_bs, c.tipo_cambio, c.codigo_verificacion
FROM cuentas_asfi c
JOIN bancos b ON c.banco_id = b.banco_id
ORDER BY c.saldo_usd DESC
LIMIT 1;

-- 4) Distribución de cuentas por algoritmo de encriptación
SELECT b.algoritmo,
       COUNT(c.cuenta_id) AS total_cuentas,
       SUM(c.saldo_usd)   AS total_usd,
       SUM(c.saldo_bs)    AS total_bs
FROM cuentas_asfi c
JOIN bancos b ON c.banco_id = b.banco_id
GROUP BY b.algoritmo
ORDER BY total_cuentas DESC;

-- 5) Promedio de saldo por entidad financiera
SELECT b.nombre,
       AVG(c.saldo_usd)   AS promedio_usd,
       AVG(c.saldo_bs)    AS promedio_bs,
       MIN(c.saldo_usd)   AS min_usd,
       MAX(c.saldo_usd)   AS max_usd
FROM cuentas_asfi c
JOIN bancos b ON c.banco_id = b.banco_id
GROUP BY b.banco_id, b.nombre
ORDER BY promedio_usd DESC;

-- 6) Top 5 cuentas con mayor diferencia USD → Bs
SELECT c.cuenta_id, c.nro_cuenta, b.nombre AS banco,
       c.saldo_usd, c.saldo_bs,
       (c.saldo_bs - c.saldo_usd) AS diferencia,
       c.tipo_cambio
FROM cuentas_asfi c
JOIN bancos b ON c.banco_id = b.banco_id
WHERE c.estado = 'convertido'
ORDER BY diferencia DESC
LIMIT 5;

-- 7) Bancos con más cuentas convertidas
SELECT b.nombre, b.algoritmo,
       COUNT(CASE WHEN c.estado = 'convertido' THEN 1 END) AS convertidas,
       COUNT(CASE WHEN c.estado = 'pendiente' THEN 1 END)  AS pendientes,
       COUNT(CASE WHEN c.estado = 'saldo_negativo' THEN 1 END) AS negativos,
       COUNT(c.cuenta_id) AS total
FROM cuentas_asfi c
JOIN bancos b ON c.banco_id = b.banco_id
GROUP BY b.banco_id, b.nombre, b.algoritmo
ORDER BY convertidas DESC;

-- 8) Últimas N entradas del log de auditoría
SELECT l.id, l.timestamp_op, l.tipo_cambio,
       l.cuenta_id, b.nombre AS banco,
       l.accion, l.detalle
FROM log_auditoria l
LEFT JOIN bancos b ON l.banco_id = b.banco_id
ORDER BY l.timestamp_op DESC
LIMIT 20;
