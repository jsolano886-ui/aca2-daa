#!/usr/bin/env bash
# Copia lógica (pg_dump) hacia el anfitrión: simula el respaldo diario del diseño (RPO).
set -eu; mkdir -p backups; f="backups/daa_$(date +%Y%m%d_%H%M%S).sql"
docker exec daa_db sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > "$f"; ls -l "$f"
# Restauración (prueba): docker exec -i daa_db sh -c 'psql -U "$POSTGRES_USER" "$POSTGRES_DB"' < backups/archivo.sql
