"""Helper module for extracting information from paycheck PDFs."""
from typing import Optional


# Constants for employee data extraction
EMPLOYEE_DATA_ROW = 2
REGISTRATION_COLUMN = -2  # Format: NAME SURNAME CODE HIRE_DATE


def extract_matricula(page_content: str) -> int:
    """
    Extract employee registration number from paycheck content.
    
    Args:
        page_content: The text content extracted from the PDF page
        
    Returns:
        int: The employee registration number, or 0 if not found
    """
    lines = page_content.split("\n")
    try:
        matricula = lines[EMPLOYEE_DATA_ROW].strip().split(" ")[REGISTRATION_COLUMN]
        return int(matricula) if matricula else 0
    except (IndexError, ValueError):
        return 0


def extract_net_salary(page_content: str) -> Optional[str]:
    """
    Extract net salary amount from paycheck content.
    
    Args:
        page_content: The text content extracted from the PDF page
        
    Returns:
        Optional[str]: The net salary amount without dots, or None if not found
    """
    lines = page_content.split("\n")
    
    for line in lines:
        if "LÍQUIDO" not in line:
            continue
            
        # Handle different paycheck formats
        if line.startswith("VALOR LÍQUIDO"):
            return line.split(" ")[2].replace(".", "")
            
        if line.startswith(" ____ /"):
            temp = line.split("LÍQUIDO")[1]
            return temp.strip().split(" ")[0].replace(".", "")
            
    return None
