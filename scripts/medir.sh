#!/usr/bin/env bash
# Mediciones para la Tabla de comparación contenedores vs. máquinas virtuales.
docker compose down >/dev/null 2>&1
echo "Imágenes:"; docker images --format '{{.Repository}}:{{.Tag}}  {{.Size}}' | grep -E 'daa-api|postgres|nginx'
t0=$(date +%s.%N); docker compose up -d >/dev/null 2>&1
until [ "$(docker inspect -f '{{.State.Health.Status}}' daa_api)" = healthy ]; do sleep 1; done
echo "Segundos hasta API healthy: $(echo "$(date +%s.%N)-$t0" | bc)"
docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}'
