"""
scripts/generate_keys.py — Genera llaves criptográficas para los 14 bancos.
Guarda en keys/keys.json. Las llaves quedan en .gitignore.

Uso: python -m scripts.generate_keys
"""
import json, os, sys, base64, secrets
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import serialization

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def b64(data: bytes) -> str:
    return base64.b64encode(data).decode()

def gen_rsa_keys():
    key = rsa.generate_private_key(65537, 2048)
    priv = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    pub = key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
    return {"private_key": priv.decode(), "public_key": pub.decode()}

def gen_ecc_keys():
    key = ec.generate_private_key(ec.SECP256R1())
    priv = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    pub = key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
    return {"private_key": priv.decode(), "public_key": pub.decode()}

def main():
    keys = {
        "1_union_cesar":       {"shift": secrets.randbelow(25) + 1},
        "2_mercantil_atbash":  {"nota": "Atbash no requiere llave (alfabeto inverso)"},
        "3_bnb_vigenere":      {"keyword": secrets.token_hex(8).upper()[:12]},
        "4_bcp_playfair":      {"keyword": secrets.token_hex(8).upper()[:10]},
        "5_bisa_hill":         {"matrix": [[secrets.randbelow(20)+1, secrets.randbelow(20)+1],
                                           [secrets.randbelow(20)+1, secrets.randbelow(20)+1]]},
        "6_ganadero_des":      {"key": b64(secrets.token_bytes(8))},
        "7_economico_3des":    {"key": b64(secrets.token_bytes(24))},
        "8_prodem_blowfish":   {"key": b64(secrets.token_bytes(16))},
        "9_solidario_twofish": {"key": b64(secrets.token_bytes(32))},
        "10_fortaleza_aes":    {"key": b64(secrets.token_bytes(32)), "iv": b64(secrets.token_bytes(16))},
        "11_fie_rsa":          gen_rsa_keys(),
        "12_pyme_elgamal":     gen_rsa_keys(),  # ElGamal simulado con RSA structure
        "13_desarrollo_ecc":   gen_ecc_keys(),
        "14_nacion_chacha20":  {"key": b64(secrets.token_bytes(32)), "nonce": b64(secrets.token_bytes(12))},
    }

    out = os.path.join(BASE, "keys", "keys.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(keys, f, indent=2, ensure_ascii=False)

    print(f"✓ Llaves generadas: {out}")
    print(f"  → {len(keys)} bancos configurados")
    for k, v in keys.items():
        tipos = [t for t in v.keys()]
        print(f"    {k}: {', '.join(tipos)}")

if __name__ == "__main__":
    main()
