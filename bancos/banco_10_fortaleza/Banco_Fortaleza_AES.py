import os
import base64
from pymongo import MongoClient
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# ============================================
# CONFIGURACIÓN AES - CLAVE CORREGIDA
# ============================================

# Clave AES de 32 bytes exactos (256 bits)
# Usamos una clave fija de 32 bytes
SECRET_KEY = b'FortalezaBank2024SecureKeyAES256'  # 32 bytes exactos

# Alternativa: Generar clave desde una contraseña (más seguro)
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# import hashlib
# password = b"mi_password_seguro"
# salt = b"sal_fija_16bytes_"  # 16 bytes
# kdf = PBKDF2HMAC(algorithm=hashlib.sha256(), length=32, salt=salt, iterations=100000)
# SECRET_KEY = kdf.derive(password)


def encrypt_aes(plaintext):
    """
    Cifra un texto con AES-256-CBC
    """
    if plaintext is None:
        return None
    
    plaintext = str(plaintext)
    
    # Generar IV aleatorio de 16 bytes
    iv = os.urandom(16)
    
    # Crear cipher
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Padding PKCS7
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
    
    # Cifrar
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    # Combinar IV + texto cifrado
    encrypted_data = iv + encrypted
    
    # Codificar en base64 para almacenamiento
    return base64.b64encode(encrypted_data).decode('utf-8')


def decrypt_aes(encrypted_text):
    """
    Descifra un texto con AES-256-CBC
    """
    if encrypted_text is None:
        return None
    
    try:
        # Decodificar base64
        encrypted_data = base64.b64decode(encrypted_text)
        
        # Extraer IV (primeros 16 bytes)
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Crear cipher para descifrar
        cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Descifrar
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remover padding
        unpadder = padding.PKCS7(128).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
        
        return decrypted.decode('utf-8')
        
    except Exception as e:
        # Si hay error, devolver el texto original (para datos no cifrados)
        return encrypted_text


# ============================================
# CONEXIÓN A MONGODB
# ============================================

# Conectar a MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Seleccionar base de datos del Banco Fortaleza
db = client['Banco_Fortaleza']

# Seleccionar colección de cuentas
collection = db['Cuentas_Fortaleza']


# ============================================
# FUNCIÓN PARA INSERTAR CUENTA CIFRADA
# ============================================

def insertar_cuenta_fortaleza(nro, identificacion, nombres, apellidos, nro_cuenta, saldo):
    """
    Inserta una cuenta en Banco Fortaleza con datos cifrados con AES
    """
    
    documento = {
        "Nro": nro,
        "Identificacion": encrypt_aes(identificacion),
        "Nombres": encrypt_aes(nombres),
        "Apellidos": encrypt_aes(apellidos),
        "NroCuenta": encrypt_aes(nro_cuenta),
        "IdBanco": 1,
        "Saldo": encrypt_aes(str(saldo)),
        "TipoCifrado": "AES-256-CBC"
    }
    
    result = collection.insert_one(documento)
    print(f"✅ Cuenta insertada con ID: {result.inserted_id}")
    print(f"   Nro: {nro} - {nombres} {apellidos} - Saldo: ${saldo}")
    print()
    
    return result.inserted_id


# ============================================
# FUNCIÓN PARA LEER CUENTAS
# ============================================

def leer_todas_cuentas():
    """
    Lee todas las cuentas y las muestra
    """
    cuentas = collection.find()
    
    print("\n" + "="*60)
    print("TODAS LAS CUENTAS DEL BANCO FORTALEZA")
    print("="*60)
    
    for cuenta in cuentas:
        print(f"\n📄 Documento ID: {cuenta['_id']}")
        print(f"   Nro: {cuenta['Nro']}")
        
        # Intentar descifrar si está cifrado
        if cuenta.get('TipoCifrado') == 'AES-256-CBC':
            identificacion = decrypt_aes(cuenta['Identificacion'])
            nombres = decrypt_aes(cuenta['Nombres'])
            apellidos = decrypt_aes(cuenta['Apellidos'])
            nro_cuenta = decrypt_aes(cuenta['NroCuenta'])
            saldo = decrypt_aes(cuenta['Saldo'])
            print(f"   Identificación: {identificacion}")
            print(f"   Nombres: {nombres}")
            print(f"   Apellidos: {apellidos}")
            print(f"   Nro Cuenta: {nro_cuenta}")
            print(f"   Saldo: ${saldo}")
            print(f"   Tipo Cifrado: {cuenta['TipoCifrado']} ✅")
        else:
            # Datos sin cifrar
            print(f"   Identificación: {cuenta.get('Identificacion', 'N/A')}")
            print(f"   Nombres: {cuenta.get('Nombres', 'N/A')}")
            print(f"   Apellidos: {cuenta.get('Apellidos', 'N/A')}")
            print(f"   Nro Cuenta: {cuenta.get('NroCuenta', 'N/A')}")
            print(f"   Saldo: ${cuenta.get('Saldo', 'N/A')}")
            print(f"   Tipo Cifrado: Sin cifrar ⚠️")
        
        print(f"   IdBanco: {cuenta['IdBanco']}")
        print("-"*40)


# ============================================
# MAIN
# ============================================

def main():
    print("="*60)
    print("🏦 BANCO FORTALEZA - CIFRADO AES-256-CBC")
    print("="*60)
    print()
    print(f"🔐 Clave AES utilizada: {len(SECRET_KEY)} bytes ({len(SECRET_KEY)*8} bits)")
    print()
    
    try:
        # Probar cifrado antes de insertar
        print("🔧 Probando cifrado...")
        test_text = "prueba123"
        encrypted = encrypt_aes(test_text)
        decrypted = decrypt_aes(encrypted)
        print(f"   Texto original: {test_text}")
        print(f"   Texto cifrado: {encrypted[:50]}...")
        print(f"   Texto descifrado: {decrypted}")
        print("   ✅ Cifrado funcionando correctamente!\n")
        
        # Insertar primer documento
        insertar_cuenta_fortaleza(
            nro=4,
            identificacion="98765432",
            nombres="Fernando Javier",
            apellidos="Rojas Silva",
            nro_cuenta="FORT9876543210123456",
            saldo=12500.5000
        )
        
        # Insertar segundo documento
        insertar_cuenta_fortaleza(
            nro=5,
            identificacion="11223344",
            nombres="Patricia Isabel",
            apellidos="Mendoza Vargas",
            nro_cuenta="FORT1122334455667788",
            saldo=325.7500
        )
        
        # Mostrar todas las cuentas
        leer_todas_cuentas()
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
    
    finally:
        # Cerrar conexión
        client.close()
        print("\n🔌 Conexión a MongoDB cerrada")


if __name__ == "__main__":
    main()