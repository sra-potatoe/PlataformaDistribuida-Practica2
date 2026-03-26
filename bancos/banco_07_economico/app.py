"""Económico (8007) — 3DES | MySQL"""
from bancos.app_factory import crear_app
app = crear_app(7)
if __name__ == "__main__":
    import uvicorn; from config import SSL_CERT, SSL_KEY
    uvicorn.run(app, host="0.0.0.0", port=8007, ssl_certfile=SSL_CERT, ssl_keyfile=SSL_KEY)
