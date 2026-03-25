use banco_fie

db.cuentas.insertMany([
    {
        "Nro": 1,
        "Identificacion": "45689234",
        "Nombres": "Ana María",
        "Apellidos": "Torrez Suárez",
        "NroCuenta": "FIE123456789012",
        "IdBanco": 2,
        "Saldo": 8750.5000
    },
    {
        "Nro": 2,
        "Identificacion": "78912345",
        "Nombres": "Roberto",
        "Apellidos": "Flores Vargas",
        "NroCuenta": "FIE987654321098",
        "IdBanco": 2,
        "Saldo": 124.3850
    },
    {
        "Nro": 3,
        "Identificacion": "12345678",
        "Nombres": "Laura Beatriz",
        "Apellidos": "Mamani Choque",
        "NroCuenta": "FIE456789123045",
        "IdBanco": 2,
        "Saldo": 2500.7500
    }
])