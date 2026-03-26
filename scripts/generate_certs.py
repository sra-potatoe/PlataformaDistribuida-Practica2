"""
scripts/generate_certs.py — Genera certificado SSL autofirmado.
Uso: python -m scripts.generate_certs
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta, timezone
import ipaddress

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    d = os.path.join(BASE, "keys", "certs"); os.makedirs(d, exist_ok=True)
    key = rsa.generate_private_key(65537, 2048)
    with open(os.path.join(d, "server.key"), "wb") as f:
        f.write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))
    subj = x509.Name([x509.NameAttribute(NameOID.COUNTRY_NAME, "BO"),
                       x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ASFI Platform"),
                       x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
    cert = (x509.CertificateBuilder().subject_name(subj).issuer_name(subj)
            .public_key(key.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(datetime.now(timezone.utc))
            .not_valid_after(datetime.now(timezone.utc) + timedelta(days=365))
            .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost"), x509.IPAddress(ipaddress.IPv4Address("127.0.0.1"))]), critical=False)
            .sign(key, hashes.SHA256()))
    with open(os.path.join(d, "server.pem"), "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    print(f"✓ Certificado: {d}/server.pem + server.key")

if __name__ == "__main__":
    main()
