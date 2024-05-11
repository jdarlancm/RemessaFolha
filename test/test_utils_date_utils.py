import pytest

from src.utils.date_utils import nome_mes


@pytest.mark.parametrize(
    "numero_do_mes, nome_do_mes", [(1, "jan"), (2, "fev"), (3, "mar")]
)
def test_nome_mes_valido(numero_do_mes, nome_do_mes):
    assert nome_mes(numero_do_mes) == nome_do_mes


@pytest.mark.parametrize("numero_do_mes", [0, 13, "invalido"])
def test_nome_mes_invalido(numero_do_mes):
    with pytest.raises(ValueError):
        nome_mes(numero_do_mes)
