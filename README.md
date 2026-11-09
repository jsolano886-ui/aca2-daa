# ACA 2 – Simulación local de la plataforma de preventa de DAA (Docker Compose)
Servicios: `gateway` (Nginx) → `api` (Flask) → `db` (PostgreSQL). Redes: `daa_front` y `daa_back` (interna).
Requisitos: Docker con Compose v2 y acceso a Docker Hub.
1. `cp .env.example .env` y cambie la contraseña.
2. `docker compose up -d --build`
3. `curl localhost:8080/health`  ·  `curl localhost:8080/productos`
4. Reglas de negocio sin Docker: `pip install pytest && pytest api/tests`
5. Evidencias: `bash scripts/verificar.sh` · Respaldo: `bash scripts/backup.sh` · Mediciones: `bash scripts/medir.sh`
6. `docker compose down` conserva datos; `docker compose down -v` borra el volumen.
Todos los datos son ficticios.
