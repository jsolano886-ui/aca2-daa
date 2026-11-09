"""API de preventa de DAA (simulación ACA 2)."""
import logging, os, time
import psycopg
from psycopg.rows import dict_row
from flask import Flask, jsonify, request
from reglas import PedidoInvalido, calcular_pedido

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/api.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("api")
app = Flask(__name__)


def conexion():
    return psycopg.connect(
        host=os.environ["DB_HOST"], port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"], user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"], row_factory=dict_row, connect_timeout=3)


@app.get("/health")
def health():
    try:
        with conexion() as c:
            c.execute("SELECT 1")
        return jsonify(estado="ok", base_de_datos="conectada", host_db=os.environ["DB_HOST"])
    except Exception as e:  # noqa: BLE001
        log.error("health: %s", e)
        return jsonify(estado="error", detalle=str(e)), 503


@app.get("/productos")
def productos():
    with conexion() as c:
        return jsonify(c.execute("SELECT sku, nombre, precio, stock FROM productos ORDER BY sku").fetchall())


@app.get("/clientes")
def clientes():
    with conexion() as c:
        return jsonify(c.execute("SELECT id, nombre, municipio FROM clientes ORDER BY id").fetchall())


@app.post("/pedidos")
def crear_pedido():
    d = request.get_json(silent=True) or {}
    with conexion() as c:
        if not c.execute("SELECT 1 FROM clientes WHERE id=%s", (d.get("cliente_id"),)).fetchone():
            return jsonify(error="cliente inexistente"), 404
        skus = [i.get("sku") for i in d.get("items", [])]
        # Bloqueo de filas para evitar vender dos veces el mismo stock
        filas = c.execute("SELECT sku, precio, stock FROM productos WHERE sku = ANY(%s) FOR UPDATE", (skus,)).fetchall()
        catalogo = {f["sku"]: {"precio": f["precio"], "stock": f["stock"]} for f in filas}
        try:
            lineas, total = calcular_pedido(d.get("items", []), catalogo)
        except PedidoInvalido as e:
            return jsonify(error=str(e)), 422
        pid = c.execute("INSERT INTO pedidos (cliente_id, total) VALUES (%s,%s) RETURNING id",
                        (d["cliente_id"], total)).fetchone()["id"]
        for l in lineas:
            c.execute("INSERT INTO pedido_items (pedido_id, sku, cantidad, precio) VALUES (%s,%s,%s,%s)",
                      (pid, l["sku"], l["cantidad"], l["precio"]))
            c.execute("UPDATE productos SET stock = stock - %s WHERE sku=%s", (l["cantidad"], l["sku"]))
    log.info("pedido %s cliente=%s total=%s", pid, d["cliente_id"], total)
    return jsonify(pedido_id=pid, total=total, lineas=lineas), 201


@app.get("/resumen")
def resumen():
    with conexion() as c:
        r = c.execute("SELECT COUNT(*) AS pedidos, COALESCE(SUM(total),0) AS ventas FROM pedidos").fetchone()
    return jsonify(pedidos=int(r["pedidos"]), ventas=int(r["ventas"]))
