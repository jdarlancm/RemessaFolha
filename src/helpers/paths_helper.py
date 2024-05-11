from dotenv import load_dotenv

from utils import date_utils
from utils import os_utils

load_dotenv()


def get_root_payroll_folder():
    payroll_folder = os_utils.get_enviroment_variable("PATH_FOLHA")
    if not payroll_folder:
        raise ValueError("A variável de ambiente PATH_FOLHA não está definida.")

    return payroll_folder


def get_payroll_year_folder(year):
    return f"{get_root_payroll_folder()}\\{year}"


def get_payroll_year_complete_filename(year):
    return f"{get_payroll_year_folder(year)}\\{get_payroll_filename()}"


def get_payroll_filename():
    return "nova_folha.xlsx"


def get_payroll_month_folder(month, year):
    return f"{get_payroll_year_folder(year)}\\{month:02d}-{date_utils.nome_mes(month)}"


def get_payroll_receipts_folder(month, year):
    return f"{get_payroll_month_folder(month, year)}\\comprovantes"


def get_payroll_receipts_folder_and_create_if_not_exists(month, year):
    receipts_path = get_payroll_receipts_folder(month, year)
    os_utils.create_path_if_not_exits(receipts_path)
    return receipts_path


def get_payroll_temp_folder(month, year):
    return f"{get_payroll_month_folder(month, year)}\\temp"


def get_payckeck_complete_filename(month, year):
    filename = f"{get_payroll_month_folder(month, year)}\\{get_paycheck_filename()}"
    if not os_utils.is_exist_file(filename):
        raise FileNotFoundError(
            f"Arquivo dos contra-cheques não encontrado: {filename}"
        )
    return filename


def get_paycheck_filename():
    return "Contra Cheque.pdf"


def get_employee_payckeck_filename(matricula, nome):
    return "{}-{}-{}".format(
        str(matricula).zfill(3), nome.upper(), get_paycheck_filename()
    )


def check_payroll_paths(month, year):
    _check_required_paths(month, year)
    _create_auxiliary_folder(month, year)


def _check_required_paths(month, year):
    root_path = get_root_payroll_folder()
    if not os_utils.is_exist_path(root_path):
        raise FileNotFoundError(f"Diretório raíz da folha não existe: {root_path}")

    payroll_path = get_payroll_month_folder(month, year)
    if not os_utils.is_exist_path(payroll_path):
        raise FileNotFoundError(f"Diretório da folha não encontrado: {payroll_path}")

    get_payckeck_complete_filename(month, year)


def _create_auxiliary_folder(month, year):
    get_payroll_receipts_folder_and_create_if_not_exists(month, year)

    temp_path = get_payroll_temp_folder(month, year)
    os_utils.create_path_if_not_exits(temp_path)
