"""
scripts/start_apis.py — Levanta todas las APIs en paralelo.
Uso: python -m scripts.start_apis
"""
import subprocess, sys, os, time
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SSL_C = os.path.join(BASE, "keys", "certs", "server.pem")
SSL_K = os.path.join(BASE, "keys", "certs", "server.key")

APIS = [(f"bancos.banco_{i:02d}_{n}.app", p, n.replace('_',' ').title()) for i, n, p in [
    (1,"union",8001),(2,"mercantil",8002),(3,"bnb",8003),(4,"bcp",8004),
    (5,"bisa",8005),(6,"ganadero",8006),(7,"economico",8007),(8,"prodem",8008),(9,"solidario",8009)]]

def main():
    print(f"{'='*50}\n  Iniciando {len(APIS)} APIs\n{'='*50}")
    procs = []
    for mod, port, name in APIS:
        cmd = [sys.executable, "-m", "uvicorn", f"{mod}:app", "--host", "0.0.0.0",
               "--port", str(port), "--ssl-certfile", SSL_C, "--ssl-keyfile", SSL_K]
        print(f"  → :{port} {name}")
        procs.append(subprocess.Popen(cmd, cwd=BASE))
        time.sleep(0.2)
    print(f"\n✓ {len(procs)} APIs activas — Ctrl+C para detener")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        for p in procs: p.terminate()
        print("\nDetenidas.")

if __name__ == "__main__":
    main()
