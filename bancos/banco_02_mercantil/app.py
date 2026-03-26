"""Banco Mercantil (8002) — Atbash | PostgreSQL"""
from bancos.app_factory import crear_app
app = crear_app(2)
if __name__ == "__main__":
    import uvicorn; from config import SSL_CERT, SSL_KEY
    uvicorn.run(app, host="0.0.0.0", port=8002, ssl_certfile=SSL_CERT, ssl_keyfile=SSL_KEY)
