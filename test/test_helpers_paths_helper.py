import pytest
import os

from helpers import paths_helper


@pytest.fixture
def patch_env(monkeypatch, tmp_path):
    monkeypatch.setenv(
        "PATH_FOLHA",
        str(tmp_path),
    )


def test_get_root_payroll_folder_variavel_ambiente_nao_definida(monkeypatch):
    monkeypatch.delenv("PATH_FOLHA", raising=False)

    with pytest.raises(ValueError) as exc_info:
        paths_helper.get_root_payroll_folder()

    error_message = str(exc_info.value)
    assert error_message == "A variável de ambiente PATH_FOLHA não está definida."


def test_get_root_payroll_folder_variavel_ambiente_definida(patch_env, tmp_path):
    root_path = paths_helper.get_root_payroll_folder()
    assert root_path == str(tmp_path)


def test_get_payroll_month_folder_mes_existente(patch_env, tmp_path):
    caminho_jan_2024 = paths_helper.get_payroll_month_folder(1, 2024)
    assert caminho_jan_2024 == rf"{tmp_path}\2024\01-jan"

    caminho_jun_2023 = paths_helper.get_payroll_month_folder(6, 2023)
    assert caminho_jun_2023 == rf"{tmp_path}\2023\06-jun"


def test_get_payroll_month_folder_mes_inexistente(patch_env, tmp_path):
    with pytest.raises(ValueError):
        paths_helper.get_payroll_month_folder(13, 2225)


def test_get_payroll_receipts_folder(patch_env, tmp_path):
    assert (
        paths_helper.get_payroll_receipts_folder(1, 2024)
        == rf"{tmp_path}\2024\01-jan\comprovantes"
    )


def test_get_payroll_temp_folder(patch_env, tmp_path):
    assert (
        paths_helper.get_payroll_temp_folder(1, 2024) == rf"{tmp_path}\2024\01-jan\temp"
    )


def test_get_payckeck_complete_filename(patch_env, tmp_path):
    paths_helper.get_payckeck_complete_filename(
        1, 2024
    ) == rf"{tmp_path}\2024\01-jan\Conta-Cheque.pdf"


def test_get_paycheck_filename():
    assert paths_helper.get_paycheck_filename() == "Contra-Cheque.pdf"


def test_check_payroll_paths_exists(patch_env, tmp_path):
    path = tmp_path / "2024" / "01-jan"
    path.mkdir(parents=True, exist_ok=True)

    path_filename = path / "Contra-Cheque.pdf"
    path_filename.touch()

    paths_helper.check_payroll_paths(1, 2024)

    assert os.path.exists(f"{path}\\comprovantes")
    assert os.path.exists(f"{path}\\temp")


def test_check_payroll_paths_not_exists(patch_env, tmp_path):
    path = tmp_path / "2024" / "01-jan"

    with pytest.raises(FileNotFoundError) as exc_info:
        paths_helper.check_payroll_paths(1, 2024)

    error_message = str(exc_info.value)
    assert error_message == f"Diretório da folha não encontrado: {path}"


def test_check_payroll_paths_root_not_exists(monkeypatch):
    path = "c:\\diretorio\\inexistente"

    monkeypatch.setenv("PATH_FOLHA", path)

    with pytest.raises(FileNotFoundError) as exc_info:
        paths_helper.check_payroll_paths(1, 2024)

    error_message = str(exc_info.value)
    assert error_message == f"Diretório raíz da folha não existe: {path}"


def test_check_payroll_paths_paycheck_file_not_exist(patch_env, tmp_path):
    path = tmp_path / "2024" / "01-jan"
    path.mkdir(parents=True, exist_ok=True)

    path_filename = path / "Contra-Cheque.pdf"
    with pytest.raises(FileNotFoundError) as exc_info:
        paths_helper.check_payroll_paths(1, 2024)

    error_message = str(exc_info.value)
    assert (
        error_message == f"Arquivo dos contra-cheques não encontrado: {path_filename}"
    )


def test_create_auxiliary_folder(patch_env, tmp_path):
    path = tmp_path / "2024" / "01-jan"
    paths_helper._create_auxiliary_folder(1, 2024)
    assert os.path.exists(f"{path}\\comprovantes")
    assert os.path.exists(f"{path}\\temp")
