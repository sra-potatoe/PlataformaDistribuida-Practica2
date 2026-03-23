"""
Banco Prodem S.A. — API (Puerto 8008)
Algoritmo: Blowfish | Motor: MySQL
"""
from bancos.app_factory import crear_app_banco
app = crear_app_banco(banco_id=8)

if __name__ == "__main__":
    import uvicorn
    from config.settings import SSL_CERTFILE, SSL_KEYFILE
    uvicorn.run(app, host="0.0.0.0", port=8008,
                ssl_certfile=SSL_CERTFILE, ssl_keyfile=SSL_KEYFILE)
