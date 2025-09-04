import os
from datetime import date
from typing import Optional

from domain.payroll import Employee
from services.gmail_service import GmailService

class NotificationService:
    """Service for handling employee notifications."""
    
    def __init__(self, gmail_service: Optional[GmailService] = None):
        self.gmail_service = gmail_service or GmailService()

    def notify_payment(self, employee: Employee, reference_date: date) -> None:
        """
        Notify an employee about their payment.
        
        Args:
            employee: The employee to notify
            reference_date: The reference date of the payment
        """
        if not employee.email:
            return
            
        subject = f"Comprovante de Pagamento - {reference_date.strftime('%m/%Y')}"
        body = self._create_notification_body(employee, reference_date)
        
        # Get both paycheck and payment receipt files
        attachments = []
        if hasattr(employee, 'paycheck') and employee.paycheck.file_path:
            # Add contra-cheque
            if os.path.exists(employee.paycheck.file_path):
                attachments.append(employee.paycheck.file_path)
            
            # Add payment receipt - same folder as paycheck but with different suffix
            receipt_path = employee.paycheck.file_path.replace("Contra-Cheque.pdf", "pagamento.pdf")
            print(receipt_path)
            if os.path.exists(receipt_path):
                attachments.append(receipt_path)
        
        if not attachments:
            print(f"Warning: No attachments found for employee {employee.name} ({employee.registration})")
            return
            
        self.gmail_service.send_email(
            to=employee.email,
            subject=subject,
            body=body,
            attachments=attachments
        )
        
    def _create_notification_body(
        self,
        employee: Employee,
        reference_date: date
    ) -> str:
        """Create the notification email body."""
        return f"""
        Prezado(a) {employee.name},

        Seu comprovante de pagamento referente ao mês {reference_date.strftime('%m/%Y')} 
        está disponível em anexo.

        Atenciosamente,
        Departamento Financeiro
        """ 