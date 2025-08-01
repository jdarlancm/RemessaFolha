from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass
class Employee:
    """Employee data for payroll processing."""
    name: str
    email: Optional[str]
    registration: str
    cpf: Optional[str] = None
    bank_account: Optional[str] = None
    bank_branch: Optional[str] = None

@dataclass
class Paycheck:
    """Represents a paycheck for an employee."""
    employee: Employee
    amount: float
    reference_date: date
    file_path: str

@dataclass
class PayrollRemittance:
    """Represents a payroll remittance batch."""
    reference_date: date
    employees: List[Employee]
    paychecks: List[Paycheck]
    total_amount: float
    batch_number: Optional[str] = None

    @property
    def reference_month(self) -> int:
        return self.reference_date.month

    @property
    def reference_year(self) -> int:
        return self.reference_date.year 