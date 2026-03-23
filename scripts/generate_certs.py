"""
scripts/generate_certs.py
Genera un certificado SSL autofirmado para las APIs.

Uso:
    python -m scripts.generate_certs
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta, timezone


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    certs_dir = os.path.join(base, "keys", "certs")
    os.makedirs(certs_dir, exist_ok=True)

    key_path = os.path.join(certs_dir, "server.key")
    cert_path = os.path.join(certs_dir, "server.pem")

    # Generar clave privada RSA 2048
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Escribir clave privada
    with open(key_path, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    # Generar certificado autofirmado
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "BO"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "La Paz"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ASFI Platform"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(__import__("ipaddress").IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )

    # Escribir certificado
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"✓ Clave privada: {key_path}")
    print(f"✓ Certificado:   {cert_path}")
    print(f"  Válido hasta:  {(datetime.now(timezone.utc) + timedelta(days=365)).strftime('%Y-%m-%d')}")


if __name__ == "__main__":
    main()
