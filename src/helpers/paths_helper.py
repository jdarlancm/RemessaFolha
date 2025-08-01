"""Helper module for managing file system paths in the payroll system."""
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

from utils import date_utils
from utils import os_utils

load_dotenv()


def get_root_payroll_folder() -> str:
    """
    Get the root folder path for payroll files from environment variables.
    
    Returns:
        str: The root folder path
        
    Raises:
        ValueError: If PATH_FOLHA environment variable is not set
    """
    payroll_folder = os_utils.get_environment_variable("PATH_FOLHA")
    if not payroll_folder:
        raise ValueError("A variável de ambiente PATH_FOLHA não está definida.")

    return payroll_folder


def get_payroll_year_folder(year: int) -> str:
    """
    Get the folder path for a specific year's payroll data.
    
    Args:
        year: The year to get the folder for
        
    Returns:
        str: The year folder path
    """
    return str(Path(get_root_payroll_folder()) / str(year))


def get_payroll_year_complete_filename(year: int) -> str:
    """
    Get the complete path to the payroll spreadsheet for a year.
    
    Args:
        year: The year to get the spreadsheet for
        
    Returns:
        str: The complete file path
    """
    return str(Path(get_payroll_year_folder(year)) / get_payroll_filename())


def get_payroll_filename() -> str:
    """Get the standard payroll spreadsheet filename."""
    return "folha.xlsx"


def get_payroll_month_folder(month: int, year: int) -> str:
    """
    Get the folder path for a specific month's payroll data.
    
    Args:
        month: The month number (1-12)
        year: The year
        
    Returns:
        str: The month folder path
    """
    month_name = date_utils.nome_mes(month)
    return str(Path(get_payroll_year_folder(year)) / f"{month:02d}-{month_name}")


def get_payroll_receipts_folder(month: int, year: int) -> str:
    """Get the folder path for payment receipts."""
    return str(Path(get_payroll_month_folder(month, year)) / "comprovantes")


def get_payroll_receipts_folder_and_create_if_not_exists(month: int, year: int) -> str:
    """
    Get the receipts folder path and create it if it doesn't exist.
    
    Args:
        month: The month number (1-12)
        year: The year
        
    Returns:
        str: The receipts folder path
    """
    receipts_path = get_payroll_receipts_folder(month, year)
    os_utils.create_path_if_not_exits(receipts_path)
    return receipts_path


def get_payroll_temp_folder(month: int, year: int) -> str:
    """Get the temporary folder path for payroll processing."""
    return str(Path(get_payroll_month_folder(month, year)) / "temp")


def get_payckeck_complete_filename(month: int, year: int) -> str:
    """
    Get the complete path to the paycheck PDF file.
    
    Args:
        month: The month number (1-12)
        year: The year
        
    Returns:
        str: The complete file path
        
    Raises:
        FileNotFoundError: If the paycheck file doesn't exist
    """
    filename = str(Path(get_payroll_month_folder(month, year)) / get_paycheck_filename())
    if not os_utils.is_exist_file(filename):
        raise FileNotFoundError(
            f"Arquivo dos contra-cheques não encontrado: {filename}"
        )
    return filename


def get_paycheck_filename() -> str:
    """Get the standard paycheck PDF filename."""
    return "Contra-Cheque.pdf"


def get_employee_payckeck_filename(matricula: int, nome: str) -> str:
    """
    Get the filename for an individual employee's paycheck.
    
    Args:
        matricula: Employee registration number
        nome: Employee name
        
    Returns:
        str: The formatted filename
    """
    return f"{str(matricula).zfill(3)}-{nome.upper()}-{get_paycheck_filename()}"


def check_payroll_paths(month: int, year: int) -> None:
    """
    Verify and setup required payroll paths.
    
    Args:
        month: The month number (1-12)
        year: The year
        
    Raises:
        FileNotFoundError: If required paths don't exist
    """
    _check_required_paths(month, year)
    _create_auxiliary_folder(month, year)


def _check_required_paths(month: int, year: int) -> None:
    """Verify that required paths exist."""
    root_path = get_root_payroll_folder()
    if not os_utils.is_exist_path(root_path):
        raise FileNotFoundError(f"Diretório raíz da folha não existe: {root_path}")

    payroll_path = get_payroll_month_folder(month, year)
    if not os_utils.is_exist_path(payroll_path):
        raise FileNotFoundError(f"Diretório da folha não encontrado: {payroll_path}")

    get_payckeck_complete_filename(month, year)


def _create_auxiliary_folder(month: int, year: int) -> None:
    """Create auxiliary folders for payroll processing."""
    get_payroll_receipts_folder_and_create_if_not_exists(month, year)

    temp_path = get_payroll_temp_folder(month, year)
    os_utils.create_path_if_not_exits(temp_path)
