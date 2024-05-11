import pytest

# from PyPDF2 import PdfWriter

# from src.main import processar_primeira_etapa


@pytest.fixture
def patch_env(monkeypatch, tmp_path):
    monkeypatch.setenv(
        "PATH_FOLHA",
        str(tmp_path),
    )


# def test_processar_primeira_etapa(patch_env):
#    processar_primeira_etapa(1, 2024)


"""

def test_dividir_contra_cheque_arquivo_existente(patch_env, tmp_path):
    # criando arquivo temporario
    path = tmp_path / "2024" / "01-jan"
    path.mkdir(parents=True, exist_ok=True)
    arquivo = path / "Contra-Cheque.pdf"

    arquivo.touch()

    dividir_contra_cheque(1, 2024)


def test_dividir_contra_cheque_arquivo_nao_existente(patch_env):
    with pytest.raises(FileNotFoundError):
        dividir_contra_cheque(1, 2025)
"""
