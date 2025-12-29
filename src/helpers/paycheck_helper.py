"""Helper module for extracting information from paycheck PDFs."""
import re
from typing import Optional


# Constants for employee data extraction
EMPLOYEE_DATA_ROW = 4
REGISTRATION_COLUMN = 1


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

        if "Valor Líquido" not in line:
            continue
        
        # Procura valor monetario no formato 1.234,56
        
        match = re.search(r'Valor\s+Líquido\s{1,2}(\d{1,3}(?:\.\d{3})*,\d{2})', line)
        if match:
            return match.group(1).replace(".", "")
                
    return None
