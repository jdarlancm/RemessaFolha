from datetime import date
from typing import List, Optional

from domain.payroll import Employee, PayrollRemittance
from repositories.payroll_repository import PayrollRepository
from services.notification_service import NotificationService
from services.spreadsheet_service import SpreadsheetService

class PayrollService:
    """Service for handling payroll processing operations."""
    
    def __init__(
        self,
        payroll_repository: PayrollRepository,
        notification_service: NotificationService,
        spreadsheet_service: Optional[SpreadsheetService] = None
    ):
        self.repository = payroll_repository
        self.notification_service = notification_service
        self.spreadsheet_service = spreadsheet_service or SpreadsheetService()

    def create_remittance(
        self,
        reference_date: date,
        unified_paycheck: bool
    ) -> PayrollRemittance:
        """
        Creates a new payroll remittance batch.
        
        Args:
            reference_date: The reference date for the payroll
            unified_paycheck: Whether paychecks are in a single file
            
        Returns:
            PayrollRemittance object with the processed batch
        """
        # Get employee data and paychecks from repository
        employees = self.repository.get_employees(reference_date)
        paychecks = self.repository.get_paychecks(reference_date, unified_paycheck)
        print("employees", employees)
        # Create remittance batch
        total = sum(paycheck.amount for paycheck in paychecks)
        batch = PayrollRemittance(
            reference_date=reference_date,
            employees=employees,
            paychecks=paychecks,
            total_amount=total
        )
        
        # Save remittance
        batch = self.repository.save_remittance(batch)
        
        # Update control sheet
        self.spreadsheet_service.update_control_sheet(batch)
        
        return batch

    def process_payment_receipts(
        self,
        reference_date: date
    ) -> None:
        """
        Process payment receipts for the given date.
        
        Args:
            reference_date: The reference date for the payroll
        """
        # Get payment return data
        remittance = self.repository.get_remittance(reference_date)
        if not remittance:
            raise ValueError(f"No remittance found for {reference_date}")
            
        # Process receipts
        self.repository.process_payment_receipts(remittance)

    def notify_employees(
        self,
        reference_date: date
    ) -> List[Employee]:
        """
        Notify employees about their payments.
        
        Args:
            reference_date: The reference date for the payroll
            
        Returns:
            List of employees that were notified
        """
        # Get payment return data
        remittance = self.repository.get_remittance(reference_date)
        if not remittance:
            raise ValueError(f"No remittance found for {reference_date}")
            
        # Notify employees
        notified = []
        for employee in remittance.employees:
            if employee.email:
                # Associar contracheque ao funcionário
                for paycheck in remittance.paychecks:
                    if paycheck.employee.registration == employee.registration:
                        employee.paycheck = paycheck
                        break
                
                #self.notification_service.notify_payment(employee, reference_date)
                notified.append(employee)
                
        return notified 