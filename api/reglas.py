"""Reglas de negocio puras del pedido de preventa (sin acceso a base de datos)."""

class PedidoInvalido(ValueError):
    pass


def calcular_pedido(items, catalogo):
    """items: [{'sku': str, 'cantidad': int}]; catalogo: {sku: {'precio': int, 'stock': int}}.
    Devuelve (lineas, total). Lanza PedidoInvalido si hay cantidades o stock inválidos."""
    if not items:
        raise PedidoInvalido("El pedido no tiene ítems")
    lineas, total, vistos = [], 0, set()
    for it in items:
        sku, cant = it.get("sku"), it.get("cantidad")
        if sku in vistos:
            raise PedidoInvalido(f"SKU repetido: {sku}")
        vistos.add(sku)
        if sku not in catalogo:
            raise PedidoInvalido(f"SKU inexistente: {sku}")
        if not isinstance(cant, int) or isinstance(cant, bool) or cant <= 0:
            raise PedidoInvalido(f"Cantidad inválida para {sku}")
        if cant > catalogo[sku]["stock"]:
            raise PedidoInvalido(f"Stock insuficiente para {sku} (disponible {catalogo[sku]['stock']})")
        sub = cant * catalogo[sku]["precio"]
        lineas.append({"sku": sku, "cantidad": cant, "precio": catalogo[sku]["precio"], "subtotal": sub})
        total += sub
    return lineas, total
