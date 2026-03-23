-- ============================================================
-- seed_bancos.sql
-- INSERT de los 14 bancos en la tabla bancos.
-- Ejecutar en CADA base de datos (solo inserta el que corresponde).
-- ============================================================

-- PostgreSQL
INSERT INTO bancos (banco_id, nombre, algoritmo_encriptacion) VALUES
(1,  'Banco Unión S.A.',                         'cesar')
ON CONFLICT (banco_id) DO NOTHING;

INSERT INTO bancos (banco_id, nombre, algoritmo_encriptacion) VALUES
(2,  'Banco Mercantil Santa Cruz S.A.',           'atbash')
ON CONFLICT (banco_id) DO NOTHING;

INSERT INTO bancos (banco_id, nombre, algoritmo_encriptacion) VALUES
(3,  'Banco Nacional de Bolivia S.A.',             'vigenere')
ON CONFLICT (banco_id) DO NOTHING;

-- SQL Server (usar MERGE o IF NOT EXISTS)
-- (4,  'Banco de Crédito de Bolivia S.A.',        'playfair')
-- (5,  'Banco BISA S.A.',                         'hill')
-- (6,  'Banco Ganadero S.A.',                     'des')

-- MySQL
-- (7,  'Banco Económico S.A.',                    '3des')
-- (8,  'Banco Prodem S.A.',                       'blowfish')
-- (9,  'Banco Solidario S.A.',                    'twofish')

-- MongoDB (gestionado por otro equipo)
-- (10, 'Banco Fortaleza S.A.',                    'aes')
-- (11, 'Banco FIE S.A.',                          'rsa')
-- (12, 'Banco PYME de la Comunidad S.A.',         'elgamal')

-- Firebase
-- (13, 'Banco de Desarrollo Productivo S.A.M.',   'ecc')
-- (14, 'Banco de la Nación Argentina',            'chacha20')
