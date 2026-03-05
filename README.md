

# Demo Docker: API + PostgreSQL + Nginx

Pequeña aplicación de ejemplo para demostrar cómo levantar un **stack completo con Docker Compose**:

* **API**: Flask (Python)
* **Base de datos**: PostgreSQL
* **Reverse proxy**: Nginx
* **Orquestación**: Docker Compose

Nginx expone la aplicación en `http://localhost:8080`.

El proxy redirige las peticiones a la API Flask, que a su vez consulta PostgreSQL.

La API depende de las librerías definidas en `requirements.txt` (`flask` y `psycopg2-binary`) .

El proxy se configura con un upstream que apunta al servicio `api` en el puerto `5000` .

---

# 1. Requisitos

Necesitas tener instalado:

* Docker
* Docker Compose (v2)

Comprobar instalación:

```bash
docker --version
docker compose version
```

---

# 2. Estructura del proyecto

```
proyecto-docker
│
├─ api
│  ├─ app.py
│  ├─ requirements.txt
│  └─ Dockerfile
│
├─ nginx
│  └─ nginx.conf
│
└─ docker-compose.yml
```

---

# 3. Levantar la aplicación

Desde la raíz del proyecto:

```bash
docker compose up -d --build
```

Esto hará:

1. Construir la imagen de la API
2. Levantar PostgreSQL
3. Levantar Nginx
4. Conectar todos los servicios mediante la red de Docker

Comprobar que todo está corriendo:

```bash
docker compose ps
```

Ver logs de la API:

```bash
docker compose logs -f api
```

---

# 4. Crear la tabla en PostgreSQL

Entramos en el contenedor de la base de datos y ejecutamos SQL.

Crear tabla:

```bash
docker compose exec db psql -U postgres -d appdb \
-c "CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);"
```

---

# 5. Insertar datos de prueba

```bash
docker compose exec db psql -U postgres -d appdb \
-c "INSERT INTO users(name) VALUES ('Ada'), ('Linus');"
```

---

# 6. Verificar datos en la base de datos

```bash
docker compose exec db psql -U postgres -d appdb \
-c "SELECT * FROM users;"
```

Salida esperada:

```
 id | name
----+-------
 1  | Ada
 2  | Linus
```

---

# 7. Probar la API

### Health check

```bash
curl http://localhost:8080/health
```

Respuesta:

```json
{"status": "ok"}
```

---

### Obtener usuarios

```bash
curl http://localhost:8080/users
```

Respuesta esperada:

```json
[
  {"id": 1, "name": "Ada"},
  {"id": 2, "name": "Linus"}
]
```

---

# 8. Parar la aplicación

Detener contenedores:

```bash
docker compose down
```

Eliminar también los volúmenes (borra la base de datos):

```bash
docker compose down -v
```

---
