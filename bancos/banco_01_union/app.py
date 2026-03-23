"""
Banco Unión S.A. — API (Puerto 8001)
Algoritmo: César | Motor: PostgreSQL
"""
from bancos.app_factory import crear_app_banco
app = crear_app_banco(banco_id=1)

if __name__ == "__main__":
    import uvicorn
    from config.settings import SSL_CERTFILE, SSL_KEYFILE
    uvicorn.run(app, host="0.0.0.0", port=8001,
                ssl_certfile=SSL_CERTFILE, ssl_keyfile=SSL_KEYFILE)
