--Para la tabla de la BD ASFI
CREATE TABLE Cuentas_TB_ASFI (
    Id_ASFI SERIAL PRIMARY KEY,
    Nombre_ASFI VARCHAR(100) NOT NULL,
    Apellidos_ASFI VARCHAR(100) NOT NULL,
    Id_banco INTEGER NOT NULL,
    NroCuenta_ASFI VARCHAR(50) UNIQUE NOT NULL,
    Saldo_Dolar DECIMAL(18, 4) NOT NULL CHECK (Saldo_Dolar >= 0),
    Saldo_Bs DECIMAL(18, 4) GENERATED ALWAYS AS (Saldo_Dolar * 6.97) STORED,
    Codigo_verificacion CHAR(8) NOT NULL,
    Fecha_Conversion DATE DEFAULT CURRENT_DATE
);

-- Insertar 5 registros 
INSERT INTO Cuentas_TB_ASFI (Nombre_ASFI, Apellidos_ASFI, Id_banco, NroCuenta_ASFI, Saldo_Dolar, Codigo_verificacion, Fecha_Conversion)
VALUES 
    -- Registro 1: Cuenta con saldo alto
    ('Juan Carlos', 'Pérez Gómez', 1, '1234567890123456', 15250.7500, 'A3F2C8D1', '2024-01-15'),
    
    -- Registro 2: Cuenta con saldo pequeño (4 decimales)
    ('María Elena', 'López Fernández', 2, '9876543210987654', 0.0009, 'B4E1D9F2', '2024-01-20'),
    
    -- Registro 3: Cuenta con saldo medio
    ('Carlos Andrés', 'Mendoza Ríos', 1, '4567891230456789', 3500.0000, 'C5D0E8A3', '2024-02-01'),
    
    -- Registro 4: Cuenta con saldo exacto
    ('Ana María', 'Torrez Suárez', 3, '7891234560789012', 8750.5000, 'D6E1F9B4', '2024-02-10'),
    
    -- Registro 5: Cuenta con saldo con 3 decimales
    ('Roberto', 'Flores Vargas', 2, '3216549870543210', 124.3850, 'E7F2A0C5', '2024-02-15');
