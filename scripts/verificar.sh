#!/usr/bin/env bash
# Evidencias del informe (capturas). Ejecutar desde la carpeta del proyecto: bash scripts/verificar.sh
set -u
H='Content-Type: application/json'
echo "### 1. Versiones";               docker --version; docker compose version
echo "### 2. Levantar";                docker compose up -d --build
echo "### 3. Estado";                  docker compose ps
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}'
echo "### 4. Redes";                   docker network ls | grep daa
for n in front back; do echo "-- daa_$n"; docker network inspect daa-sim_daa_$n --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'; done
echo "### 5. DNS interno api -> db";   docker exec daa_api python -c "import socket;print('db =',socket.gethostbyname('db'))"
echo "### 6. Salud";                   curl -s localhost:8080/health; echo
echo "### 7. Catálogo";                curl -s localhost:8080/productos; echo
echo "### 8. Pedido válido";           curl -s -X POST localhost:8080/pedidos -H "$H" -d '{"cliente_id":1,"items":[{"sku":"ARR-500","cantidad":20},{"sku":"ACE-1L","cantidad":5}]}'; echo
echo "### 9. Pedido inválido (stock)"; curl -s -X POST localhost:8080/pedidos -H "$H" -d '{"cliente_id":1,"items":[{"sku":"ATU-170","cantidad":9999}]}'; echo
echo "### 10. Resumen";                curl -s localhost:8080/resumen; echo
echo "### 11. Aislamiento";            (timeout 3 bash -c '</dev/tcp/127.0.0.1/5432' && echo "5432 ABIERTO") || echo "5432 cerrado en el anfitrión (correcto)"
docker exec daa_db wget -T3 -qO- http://1.1.1.1 >/dev/null 2>&1 && echo "db con salida a internet" || echo "db sin salida a internet (red interna)"
echo "### 12. Persistencia: down (sin -v) y up"
docker compose down; docker volume ls | grep daa; docker compose up -d
until [ "$(docker inspect -f '{{.State.Health.Status}}' daa_api)" = healthy ]; do sleep 2; done
curl -s localhost:8080/resumen; echo
echo "### 13. Volumen y bind mounts"; docker volume inspect daa-sim_daa_pgdata --format '{{.Mountpoint}}'; ls -l logs/
