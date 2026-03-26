# Plataforma Distribuida de Conversión Monetaria Interbancaria – ASFI

Este repositorio contiene la **infraestructura base, las APIs y los microservicios** para la Práctica 2 de Sistemas Distribuidos (Conversión Monetaria de USD a Bs de 14 entidades financieras).

El proyecto fue diseñado con arquitectura de microservicios, seguridad criptográfica, validación estricta y auditoría transversal.

---

## 🏗️ Lo que ya está implementado (En este repositorio)

1. **Jerarquía y Configuración Central** (`config/settings.py`):
   Maneja las variables de entorno para 14 bancos, motores de bases de datos, claves JWT, tipo de cambio y Neo4j.

2. **Esquemas de Base de Datos** (`sql/`):
   Archivos SQL listos para crear las tablas (`bancos`, `cuentas`, `audit_log`) en PostgreSQL, SQL Server y MySQL. Incluye la BD central de ASFI (`schema_asfi.sql`) y la carga inicial (semilla) de los bancos.

3. **Módulos Compartidos** (`bancos/`):
   - Conexiones a bases de datos cacheadas (SQLAlchemy).
   - Middleware de seguridad JWT, firmas HMAC y prevención de ataques Replay (Nonce + Timestamp).
   - Validaciones estrictas de los campos del CSV.
   - Funciones de auditoría (registra cualquier INSERT, UPDATE, API Access o conversión).

4. **9 APIs de Bancos (Microservicios)** (`bancos/banco_XX/app.py`):
   Servicios FastAPI levantados en los puertos 8001 al 8009 simulando 9 bancos diferentes, exponiendo endpoints seguros (`GET /info`, `GET /cuentas`, `POST /verificar`).

5. **Servicio de Tipo de Cambio** (`asfi/services/tipo_cambio.py`):
   Servidor independiente (pto 8100) que simula la fluctuación del dólar mediante un CRON interno (APScheduler) cada 3 minutos, variando ±0.9999. Incluye firma HMAC para anti-tampering.

6. **Neo4j — Base de Datos de Grafos** (`neo4j/populate_graph.py`):
   Script de carga masiva (batch) que lee las cuentas de PostgreSQL y genera la red `(:Cliente)-[:TIENE_CUENTA]->(:Cuenta)`.

7. **8 Consultas SQL (Integración)** (`sql/consultas.sql`):
   Consultas avanzadas en crudo sobre la base de datos de ASFI de acuerdo con la rúbrica (agrupaciones por banco, max saldos, diferencias de conversión, logs, etc.).

8. **Verificación de Consistencia** (`scripts/validar_consistencia.py`):
   Script que lee BD a BD (banco por banco) comparando con el conteo de la ASFI, avisando si existen diferencias en el número de cuentas o en dinero (hasta el centavo) y loguea el reporte.

9. **Scripts Utilitarios** (`scripts/`):
   Generación nativa de llaves criptográficas modernas (RSA, ECC, AES, etc.) mediante Python crudo, generador de un certificado Autofirmado SSL local y lanzador masivo en Threads (`start_apis.py`). Y un testeador paralelo (`barrido_paralelo.py`).

---

## 🚨 Lo que FALTA por implementar (Trabajo Restante)

Para llegar a los 130 puntos, este repositorio necesita combinarse con el trabajo del resto del equipo. Falta específicamente:

### 1. Módulo `crypto/` (Responsable: Erika)
- Falta la carpeta con las **14 clases en Python** que implementen en código los algoritmos exigidos (César, Atbash, Vigenère, Playfair, Hill, DES, 3DES, Blowfish, Twofish, AES, RSA, ElGamal, ECC, ChaCha20).
- Estas clases deben tener funciones estándar como `encrypt(texto_plano) -> texto_cifrado` y `decrypt(texto_cifrado) -> texto_plano` para que este repositorio las mande a llamar.

### 2. Dataset Oficial y Scripts de Poblado (Responsable: Andy/Samuel)
- Falta el archivo `cuentas.csv` original del Google Drive.
- Faltan los scripts temporales (ej. `populate_pg.py`, `populate_mysql.py`) que:
  1. Lean ese CSV inmenso en trozos (chunks).
  2. Llamen a la función `encrypt()` del módulo `crypto/`.
  3. Inserten los datos cifrados a las diferentes bases de datos recién creadas mediante SQLAlchemy. (Estos insertados deben detonar un insert automático a `audit_log`).

### 3. Servicio Receptor Orchestrador "Mini-ASFI" (Responsable: Cualquier miembro)
Falta el macro proceso (el "orquestador líder"). Necesitan hacer un script independiente que junte todas las piezas del rompecabezas. Debería funcionar así:
1. Pida el Token JWT usando la firma que ya está programada.
2. Hacer GET Masivo a las 14 APIs (Puertos 8001 a 8014).
3. Agarrar la data encriptada, llamar a las llaves maestras en `keys/keys.json` y pasarlas por el módulo `crypto/` para desencriptar en memoria.
4. Consultar `http://localhost:8100/tipo-cambio` y obtener el valor del dólar exacto en ese nanosegundo.
5. Multiplicar `saldoUSD * tipo_cambio`.
6. Enviar ese resultado a través de un `POST /verificar` a la API de cada banco.
7. Guardar una copia central ya en bolivianos de forma plana en la BD PostgreSQL (Con tabla `cuentas_asfi` que ya armé en `schema_asfi.sql`).

---

## 🤝 Cómo Integrar (Paso a paso para el resto del equipo)

Si otro miembro del equipo clonó este repo y quiere agregar lo suyo, debe seguir estos pasos en orden:

### Paso A: Entorno Básico
1. Clonar el repositorio.
2. Crear su propio entorno virtual e instalar las librerías:
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   pip install -r Requirements.txt
   ```
3. Generar la configuración local:
   Copiar el archivo `config/.env.example` y renombrarlo como `config/.env`. Llenar su usuario, contraseña de PostgreSQL, MySQL y SQL Server.
4. Generar las llaves locales:
   Hacer `python -m scripts.generate_keys` (Creará el `keys.json`).
5. Generar los Certificados HTTPS fake para que las APIs levanten seguras:
   Hacer `python -m scripts.generate_certs` (Creará los `.pem` y `.key`).

### Paso B: Integración Criptográfica (`crypto/`)
1. El encargado de seguridad debe meter todos sus algoritmos en la raíz de la carpeta `crypto/`.
2. Crear un archivo general `crypto/main.py` o en el `__init__.py` con una clase unificada o funciones fáciles de usar, por ejemplo:
   ```python
   def desencriptar_campo(texto_cifrado, algoritmo, banco_id, keys_json):
       # Lógica condicional aquí
       pass
   ```

### Paso C: Llenar las BD Reales
1. Montar en sus computadoras servicios (o Docker) para PostgreSQL (Pt 5432), Server (Pt 1433) y MySQL (3306).
2. Entrar a cada uno y correr a mano el código que dejé en la carpeta `sql/` para que existan las tablas. (Asegúrese de correr el `seed_bancos.sql`).
3. Crear y ejecutar el Script de poblado (`populate.py`) que usa la librería nativa de su motor para inyectar un 1% de todo el CSV con la data ya cifrada por el Paso B.

### Paso D: Encender los Motores
Solo cuando las BD tengan datos, ya funcionarán de verdad las APIs.
Tienen que ejecutar: `python -m scripts.start_apis` y mágicamente saldrán 9 hilos ejecutando 9 servidores FASTApi seguros.
Desde una terminal CURL o probando Postman podrían hacerle peticiones HTTPS de autenticación de forma pura y controlada.

*(Para el equipo encargado de MongoDB (bancos 10-12) y el de Firebase (bancos 13-14) tienen que agregar sus APIs siguiendo el molde sencillo de 2 líneas de código mostrado en mis endpoints `banco_XX_nombre/app.py`)*

### Resumen final
La arquitectura está puesta y lista como si fuesen andamios gigantescos alrededor de una obra. Ya tienen tuberías de red, cables de autenticación de seguridad, cascos (criptografía TLS), bases de cimientos (Log de Auditoría unificado). Ahora el equipo literal tiene que arrojar el cemento encima (El Script que mete las miles de filas y la decodificación masiva).
