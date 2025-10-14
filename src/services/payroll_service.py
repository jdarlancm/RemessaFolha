from datetime import date
from typing import List, Optional

from domain.payroll import Employee, PayrollRemittance, Paycheck
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
            List of employees that were successfully notified
        """
        # Get payment return data
        remittance = self.repository.get_remittance(reference_date)
        if not remittance:
            raise ValueError(f"No remittance found for {reference_date}")
            
        # Notify employees
        notified = []
        failed_notifications = []
        skipped_no_email = []
        skipped_no_paycheck = []
        
        for employee in remittance.employees:
            if not employee.email:
                skipped_no_email.append(employee)
                print(f"SK {employee.name} ({employee.registration}) - Skipping - no email")
                continue
                
            # Associate paycheck with employee (create a copy to avoid mutation)
            employee_with_paycheck = self._associate_paycheck(employee, remittance.paychecks)
            
            if not employee_with_paycheck:
                skipped_no_paycheck.append(employee)
                print(f"SK {employee.name} ({employee.registration}) - Skipping - no paycheck found")
                continue
                
            try:
                success = self.notification_service.notify_payment(employee_with_paycheck, reference_date)
                if success:
                    notified.append(employee_with_paycheck)
                else:
                    failed_notifications.append(employee_with_paycheck)
                    print(f"ER {employee.name} ({employee.registration}) - Ocorreu um erro - Falha ao preparar email")
                    
            except Exception as e:
                failed_notifications.append(employee_with_paycheck)
                print(f"ER {employee.name} ({employee.registration}) - Ocorreu um erro - {str(e)}")
                
        # Summary
        print(f"\nResumo dos e-mails:")
        print(f"  OK - Preparados com sucesso: {len(notified)}")
        
        if skipped_no_email:
            print(f"  Pulados sem e-mail: {len(skipped_no_email)}")
            
        if skipped_no_paycheck:
            print(f"  Pulados sem contracheque: {len(skipped_no_paycheck)}")
            
        if failed_notifications:
            print(f"  ERRO - Falharam na preparação: {len(failed_notifications)}")
                
        print(f"{len(notified)} funcionários notificados.")
                
        return notified
    
    def _associate_paycheck(self, employee: Employee, paychecks: List[Paycheck]) -> Optional[Employee]:
        """
        Associate paycheck with employee without mutating the original employee.
        
        Args:
            employee: The employee to associate paycheck with
            paychecks: List of available paychecks
            
        Returns:
            Employee with associated paycheck or None if not found
        """
        for paycheck in paychecks:
            if paycheck.employee.registration == employee.registration:
                # Create a copy of the employee to avoid mutation
                employee_copy = Employee(
                    name=employee.name,
                    email=employee.email,
                    registration=employee.registration,
                    cpf=employee.cpf,
                    bank_account=employee.bank_account,
                    bank_branch=employee.bank_branch
                )
                employee_copy.paycheck = paycheck
                return employee_copy
                
        return None 