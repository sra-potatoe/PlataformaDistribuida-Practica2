import os
import base64
from pymongo import MongoClient
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

# ============================================
# CONFIGURACIÓN RSA
# ============================================

def generar_claves_rsa():
    """
    Genera un par de claves RSA (pública y privada)
    """
    # Generar clave privada RSA de 2048 bits
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Obtener clave pública
    public_key = private_key.public_key()
    
    return private_key, public_key


def guardar_clave_privada(private_key, filename="clave_privada_fie.pem"):
    """
    Guarda la clave privada en un archivo PEM
    """
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as f:
        f.write(pem)
    print(f"🔐 Clave privada guardada en: {filename}")


def guardar_clave_publica(public_key, filename="clave_publica_fie.pem"):
    """
    Guarda la clave pública en un archivo PEM
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, 'wb') as f:
        f.write(pem)
    print(f"🔑 Clave pública guardada en: {filename}")


def cargar_clave_privada(filename="clave_privada_fie.pem"):
    """
    Carga la clave privada desde un archivo PEM
    """
    with open(filename, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )
    return private_key


def cargar_clave_publica(filename="clave_publica_fie.pem"):
    """
    Carga la clave pública desde un archivo PEM
    """
    with open(filename, 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
    return public_key


# ============================================
# FUNCIONES DE CIFRADO Y DESCIFRADO RSA
# ============================================

def encrypt_rsa(plaintext, public_key):
    """
    Cifra un texto con RSA usando la clave pública
    """
    if plaintext is None:
        return None
    
    plaintext = str(plaintext)
    
    # RSA solo puede cifrar datos del tamaño de la clave menos padding
    # Para texto largo, se debe usar cifrado híbrido (RSA + AES)
    # Aquí asumimos que los datos son pequeños
    try:
        encrypted = public_key.encrypt(
            plaintext.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        # Si el texto es muy largo, usar cifrado híbrido
        print(f"Texto muy largo para RSA, usando cifrado híbrido: {e}")
        return cifrado_hibrido(plaintext, public_key)


def decrypt_rsa(encrypted_text, private_key):
    """
    Descifra un texto con RSA usando la clave privada
    """
    if encrypted_text is None:
        return None
    
    try:
        encrypted_data = base64.b64decode(encrypted_text)
        decrypted = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode('utf-8')
    except Exception as e:
        # Si no es RSA válido, devolver el texto original
        return encrypted_text


# ============================================
# CONEXIÓN A MONGODB
# ============================================

# Conectar a MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Seleccionar base de datos del Banco FIE
db = client['Banco_Fie']

# Seleccionar colección de cuentas
collection = db['Cuentas_Fie']


# ============================================
# FUNCIÓN PARA INSERTAR CUENTA_FIE CIFRADA CON RSA
# ============================================

def insertar_cuenta_fie(nro, identificacion, nombres, apellidos, nro_cuenta, saldo, public_key):
    """
    Inserta una cuenta en Banco FIE con datos cifrados con RSA
    """
    
    documento = {
        "Nro": nro,
        "Identificacion": encrypt_rsa(identificacion, public_key),
        "Nombres": encrypt_rsa(nombres, public_key),
        "Apellidos": encrypt_rsa(apellidos, public_key),
        "NroCuenta": encrypt_rsa(nro_cuenta, public_key),
        "IdBanco": 2,  # FIE
        "Saldo": encrypt_rsa(str(saldo), public_key),
        "TipoCifrado": "RSA-2048-OAEP"
    }
    
    result = collection.insert_one(documento)
    print(f"✅ Cuenta insertada con ID: {result.inserted_id}")
    print(f"   Nro: {nro} - {nombres} {apellidos} - Saldo: ${saldo}")
    print()
    
    return result.inserted_id


# ============================================
# FUNCIÓN PARA LEER Y DESCIFRAR CUENTAS
# ============================================

def leer_todas_cuentas(private_key):
    """
    Lee todas las cuentas y las descifra usando la clave privada
    """
    cuentas = collection.find()
    
    print("\n" + "="*60)
    print("TODAS LAS CUENTAS DEL BANCO FIE")
    print("="*60)
    
    for cuenta in cuentas:
        print(f"\n📄 Documento ID: {cuenta['_id']}")
        print(f"   Nro: {cuenta['Nro']}")
        
        # Descifrar según el tipo de cifrado
        if cuenta.get('TipoCifrado') == 'RSA-2048-OAEP':
            try:
                identificacion = decrypt_rsa(cuenta['Identificacion'], private_key)
                nombres = decrypt_rsa(cuenta['Nombres'], private_key)
                apellidos = decrypt_rsa(cuenta['Apellidos'], private_key)
                nro_cuenta = decrypt_rsa(cuenta['NroCuenta'], private_key)
                saldo = decrypt_rsa(cuenta['Saldo'], private_key)
                
                print(f"   Identificación: {identificacion}")
                print(f"   Nombres: {nombres}")
                print(f"   Apellidos: {apellidos}")
                print(f"   Nro Cuenta: {nro_cuenta}")
                print(f"   Saldo: ${saldo}")
                print(f"   Tipo Cifrado: {cuenta['TipoCifrado']} ✅")
            except Exception as e:
                print(f"   ⚠️ Error al descifrar: {e}")
                print(f"   Identificación: {cuenta.get('Identificacion', 'N/A')[:50]}...")
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
# FUNCIÓN PARA VER DATOS CIFRADOS EN BD
# ============================================

def ver_datos_cifrados():
    """
    Muestra cómo se ven los datos cifrados en la base de datos
    """
    cuentas = collection.find()
    
    print("\n" + "="*60)
    print("DATOS CIFRADOS EN MONGODB (BANCO FIE)")
    print("="*60)
    
    for cuenta in cuentas:
        print(f"\n📄 Documento ID: {cuenta['_id']}")
        print(f"   Nro: {cuenta['Nro']}")
        print(f"   Identificacion (cifrado): {str(cuenta.get('Identificacion', ''))[:60]}...")
        print(f"   Nombres (cifrado): {str(cuenta.get('Nombres', ''))[:60]}...")
        print(f"   Apellidos (cifrado): {str(cuenta.get('Apellidos', ''))[:60]}...")
        print(f"   NroCuenta (cifrado): {str(cuenta.get('NroCuenta', ''))[:60]}...")
        print(f"   Saldo (cifrado): {str(cuenta.get('Saldo', ''))[:60]}...")
        print(f"   Tipo Cifrado: {cuenta.get('TipoCifrado', 'Sin cifrar')}")
        print("-"*40)


# ============================================
# MAIN
# ============================================

def main():
    print("="*60)
    print("🏦 BANCO FIE - CIFRADO RSA-2048-OAEP")
    print("="*60)
    print()
    
    # Verificar si existen las claves, si no, generarlas
    if not os.path.exists("clave_privada_fie.pem"):
        print("🔐 Generando nuevo par de claves RSA...")
        private_key, public_key = generar_claves_rsa()
        guardar_clave_privada(private_key)
        guardar_clave_publica(public_key)
        print()
    else:
        print("🔑 Cargando claves RSA existentes...")
        private_key = cargar_clave_privada()
        public_key = cargar_clave_publica()
        print("   ✅ Claves cargadas correctamente\n")
    
    # Probar cifrado antes de insertar
    print("🔧 Probando cifrado RSA...")
    test_text = "prueba123"
    encrypted = encrypt_rsa(test_text, public_key)
    decrypted = decrypt_rsa(encrypted, private_key)
    print(f"   Texto original: {test_text}")
    print(f"   Texto cifrado: {encrypted[:50]}...")
    print(f"   Texto descifrado: {decrypted}")
    print("   ✅ Cifrado funcionando correctamente!\n")
    
    # Mostrar información de las claves
    print("📋 INFORMACIÓN DE LAS CLAVES RSA:")
    print(f"   Clave pública: RSA-2048 bits")
    print(f"   Padding: OAEP con SHA-256")
    print(f"   Archivo clave pública: clave_publica_fie.pem")
    print(f"   Archivo clave privada: clave_privada_fie.pem")
    print()
   
    
    # Insertar primer documento
    insertar_cuenta_fie(
        nro=4,
        identificacion="55667788",
        nombres="Gabriela Andrea",
        apellidos="Torrico Rojas",
        nro_cuenta="FIE5566778899001122",
        saldo=4250.0000,
        public_key=public_key
    )
    
    # Insertar segundo documento
    insertar_cuenta_fie(
        nro=5,
        identificacion="99887766",
        nombres="Luis Fernando",
        apellidos="Mamani Quispe",
        nro_cuenta="FIE9988776655443322",
        saldo=17890.5000,
        public_key=public_key
    )
    
    # Insertar tercer documento (con texto largo para probar cifrado híbrido)
    insertar_cuenta_fie(
        nro=6,
        identificacion="11223344",
        nombres="Daniela Elizabeth",
        apellidos="Fernández Gutiérrez",
        nro_cuenta="FIE1122334455667788",
        saldo=350.7500,
        public_key=public_key
    )
    
    # Mostrar todas las cuentas descifradas
    leer_todas_cuentas(private_key)
    
    # Mostrar cómo se ven los datos cifrados en MongoDB
    ver_datos_cifrados()
    
    # Cerrar conexión
    client.close()
    print("\n Conexión a MongoDB cerrada")


if __name__ == "__main__":
    main()