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
    import re
    
    lines = page_content.split("\n")
    
    for line in lines:
        if "VALOR LÍQUIDO" in line:
            # Procura por um padrão de número com ponto e vírgula após "VALOR LÍQUIDO"
            match = re.search(r'VALOR\s+LÍQUIDO\s+(\d{1,3}(?:\.\d{3})*,\d{2})', line)
            if match:
                value = match.group(1)
                # Remove os pontos mantendo a vírgula
                return value.replace(".", "")
                
    return None
