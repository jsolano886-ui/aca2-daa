import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pytest
from reglas import calcular_pedido, PedidoInvalido
CAT = {"A": {"precio": 1000, "stock": 10}, "B": {"precio": 500, "stock": 2}}

def test_total():
    l, t = calcular_pedido([{"sku": "A", "cantidad": 3}, {"sku": "B", "cantidad": 2}], CAT)
    assert t == 4000 and len(l) == 2
@pytest.mark.parametrize("items", [[], [{"sku": "Z", "cantidad": 1}], [{"sku": "A", "cantidad": 0}],
    [{"sku": "A", "cantidad": 11}], [{"sku": "A", "cantidad": True}],
    [{"sku": "A", "cantidad": 1}, {"sku": "A", "cantidad": 1}]])
def test_invalidos(items):
    with pytest.raises(PedidoInvalido):
        calcular_pedido(items, CAT)
