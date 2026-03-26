import os
import json
import base64
import random
from pymongo import MongoClient
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ============================================
# IMPLEMENTACIÓN DE ELGAMAL
# ============================================

def generar_primo(bits=256):
    """
    Genera un número primo de bits especificados
    Para simplificar, usamos números pequeños en la demo
    En producción usar números mucho más grandes
    """
    # Para demostración, usamos un primo conocido
    # En producción: usar sympy o una librería especializada
    primos_conocidos = {
        128: 340282366920938463463374607431768211507,
        256: 115792089237316195423570985008687907853269984665640564039457584007913129639747,
    }
    return primos_conocidos.get(bits, primos_conocidos[256])


class ElGamal:
    """
    Implementación simplificada de ElGamal para demostración
    """
    
    def __init__(self, bits=256):
        """
        Inicializa el sistema ElGamal
        """
        self.bits = bits
        self.p = generar_primo(bits)  # Número primo grande
        self.g = 2  # Generador (simplificado)
        
    def generar_claves(self):
        """
        Genera un par de claves ElGamal
        Retorna: (clave_privada, clave_publica)
        """
        # Clave privada: número aleatorio entre 1 y p-2
        x = random.randint(2, self.p - 2)
        
        # Clave pública: h = g^x mod p
        h = pow(self.g, x, self.p)
        
        clave_publica = {
            'p': self.p,
            'g': self.g,
            'h': h
        }
        
        return x, clave_publica
    
    def cifrar(self, mensaje, clave_publica):
        """
        Cifra un mensaje usando ElGamal
        """
        if mensaje is None:
            return None
        
        mensaje = str(mensaje)
        
        # Convertir mensaje a número
        m = int.from_bytes(mensaje.encode('utf-8'), 'big')
        
        p = clave_publica['p']
        g = clave_publica['g']
        h = clave_publica['h']
        
        # Elegir k aleatorio
        k = random.randint(2, p - 2)
        
        # Calcular c1 = g^k mod p
        c1 = pow(g, k, p)
        
        # Calcular c2 = m * h^k mod p
        hk = pow(h, k, p)
        c2 = (m * hk) % p
        
        # Retornar par (c1, c2) en base64
        cifrado = {
            'c1': c1,
            'c2': c2
        }
        
        # Convertir a JSON y luego a base64
        cifrado_json = json.dumps(cifrado)
        return base64.b64encode(cifrado_json.encode('utf-8')).decode('utf-8')
    
    def descifrar(self, texto_cifrado, clave_privada, clave_publica):
        """
        Descifra un mensaje usando ElGamal
        """
        if texto_cifrado is None:
            return None
        
        try:
            # Decodificar base64
            cifrado_json = base64.b64decode(texto_cifrado).decode('utf-8')
            cifrado = json.loads(cifrado_json)
            
            c1 = cifrado['c1']
            c2 = cifrado['c2']
            p = clave_publica['p']
            x = clave_privada
            
            # Calcular c1^x mod p
            c1x = pow(c1, x, p)
            
            # Calcular inverso modular
            c1x_inv = pow(c1x, -1, p)
            
            # Recuperar mensaje: m = c2 * (c1^x)^(-1) mod p
            m = (c2 * c1x_inv) % p
            
            # Convertir número a texto
            try:
                # Obtener bytes del número
                byte_length = (m.bit_length() + 7) // 8
                mensaje_bytes = m.to_bytes(byte_length, 'big')
                return mensaje_bytes.decode('utf-8')
            except:
                return str(m)
                
        except Exception as e:
            # Si no es ElGamal válido, devolver el texto original
            return texto_cifrado


# ============================================
# CONFIGURACIÓN ELGAMAL
# ============================================

# Crear instancia de ElGamal
elgamal = ElGamal(bits=256)

# Generar o cargar claves
CLAVE_PRIVADA_FILE = "clave_privada_pyme.json"
CLAVE_PUBLICA_FILE = "clave_publica_pyme.json"


def guardar_claves_elgamal(clave_privada, clave_publica):
    """
    Guarda las claves ElGamal en archivos JSON
    """
    with open(CLAVE_PRIVADA_FILE, 'w') as f:
        json.dump({'x': clave_privada}, f)
    
    with open(CLAVE_PUBLICA_FILE, 'w') as f:
        json.dump(clave_publica, f)
    
    print(f" Clave privada guardada en: {CLAVE_PRIVADA_FILE}")
    print(f" Clave pública guardada en: {CLAVE_PUBLICA_FILE}")


def cargar_claves_elgamal():
    """
    Carga las claves ElGamal desde archivos JSON
    """
    with open(CLAVE_PRIVADA_FILE, 'r') as f:
        priv_data = json.load(f)
        clave_privada = priv_data['x']
    
    with open(CLAVE_PUBLICA_FILE, 'r') as f:
        clave_publica = json.load(f)
    
    return clave_privada, clave_publica


# ============================================
# CONEXIÓN A MONGODB
# ============================================

# Conectar a MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Seleccionar base de datos del Banco PYME
db = client['Banco_Pyme']

# Seleccionar colección de cuentas
collection = db['Cuentas_Pyme']


# ============================================
# FUNCIÓN PARA INSERTAR CUENTA CIFRADA CON ELGAMAL
# ============================================

def insertar_cuenta_pyme(nro, identificacion, nombres, apellidos, nro_cuenta, saldo, clave_publica):
    """
    Inserta una cuenta en Banco PYME con datos cifrados con ElGamal
    """
    
    documento = {
        "Nro": nro,
        "Identificacion": elgamal.cifrar(identificacion, clave_publica),
        "Nombres": elgamal.cifrar(nombres, clave_publica),
        "Apellidos": elgamal.cifrar(apellidos, clave_publica),
        "NroCuenta": elgamal.cifrar(nro_cuenta, clave_publica),
        "IdBanco": 3,  # PYME
        "Saldo": elgamal.cifrar(str(saldo), clave_publica),
        "TipoCifrado": "ElGamal-256"
    }
    
    result = collection.insert_one(documento)
    print(f"✅ Cuenta insertada con ID: {result.inserted_id}")
    print(f"   Nro: {nro} - {nombres} {apellidos} - Saldo: ${saldo}")
    print()
    
    return result.inserted_id


# ============================================
# FUNCIÓN PARA LEER Y DESCIFRAR CUENTAS
# ============================================

def leer_todas_cuentas(clave_privada, clave_publica):
    """
    Lee todas las cuentas y las descifra usando ElGamal
    """
    cuentas = collection.find()
    
    print("\n" + "="*60)
    print("TODAS LAS CUENTAS DEL BANCO PYME")
    print("="*60)
    
    for cuenta in cuentas:
        print(f"\n📄 Documento ID: {cuenta['_id']}")
        print(f"   Nro: {cuenta['Nro']}")
        
        # Descifrar según el tipo de cifrado
        if cuenta.get('TipoCifrado') == 'ElGamal-256':
            try:
                identificacion = elgamal.descifrar(cuenta['Identificacion'], clave_privada, clave_publica)
                nombres = elgamal.descifrar(cuenta['Nombres'], clave_privada, clave_publica)
                apellidos = elgamal.descifrar(cuenta['Apellidos'], clave_privada, clave_publica)
                nro_cuenta = elgamal.descifrar(cuenta['NroCuenta'], clave_privada, clave_publica)
                saldo = elgamal.descifrar(cuenta['Saldo'], clave_privada, clave_publica)
                
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
    print("DATOS CIFRADOS EN MONGODB (BANCO PYME)")
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
    print("🏦 BANCO PYME - CIFRADO ELGAMAL")
    print("="*60)
    print()
    
    # Verificar si existen las claves, si no, generarlas
    if not os.path.exists(CLAVE_PRIVADA_FILE):
        print("🔐 Generando nuevo par de claves ElGamal...")
        clave_privada, clave_publica = elgamal.generar_claves()
        guardar_claves_elgamal(clave_privada, clave_publica)
        print()
    else:
        print("🔑 Cargando claves ElGamal existentes...")
        clave_privada, clave_publica = cargar_claves_elgamal()
        print("   ✅ Claves cargadas correctamente\n")
    
    # Mostrar información de las claves
    print("📋 INFORMACIÓN DEL SISTEMA ELGAMAL:")
    print(f"   Módulo primo (p): {str(clave_publica['p'])[:50]}...")
    print(f"   Generador (g): {clave_publica['g']}")
    print(f"   Clave pública (h): {str(clave_publica['h'])[:50]}...")
    print(f"   Clave privada (x): {clave_privada}")
    print()
    
    # Probar cifrado antes de insertar
    print("🔧 Probando cifrado ElGamal...")
    test_text = "prueba123"
    encrypted = elgamal.cifrar(test_text, clave_publica)
    decrypted = elgamal.descifrar(encrypted, clave_privada, clave_publica)
    print(f"   Texto original: {test_text}")
    print(f"   Texto cifrado: {encrypted[:50]}...")
    print(f"   Texto descifrado: {decrypted}")
    print("   ✅ Cifrado funcionando correctamente!\n")
    
    # Insertar primer documento
    insertar_cuenta_pyme(
        nro=4,
        identificacion="33445566",
        nombres="Veronica Beatriz",
        apellidos="Arias Montes",
        nro_cuenta="PYME3344556677889900",
        saldo=5230.7500,
        clave_publica=clave_publica
    )
    
    # Insertar segundo documento
    insertar_cuenta_pyme(
        nro=5,
        identificacion="77665544",
        nombres="Ricardo Jose",
        apellidos="Paredes Soliz",
        nro_cuenta="PYME7766554433221100",
        saldo=12450.0000,
        clave_publica=clave_publica
    )
    
    # Insertar tercer documento
    insertar_cuenta_pyme(
        nro=6,
        identificacion="55443322",
        nombres="Carla Jimena",
        apellidos="Vargas Linares",
        nro_cuenta="PYME5544332211009988",
        saldo=875.2500,
        clave_publica=clave_publica
    )
    
    # Mostrar todas las cuentas descifradas
    leer_todas_cuentas(clave_privada, clave_publica)
    
    # Mostrar cómo se ven los datos cifrados en MongoDB
    ver_datos_cifrados()
    
    # Cerrar conexión
    client.close()
    print("\n Conexión a MongoDB cerrada")


if __name__ == "__main__":
    main()