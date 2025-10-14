import os
import logging
from datetime import date
from typing import Optional

from domain.payroll import Employee
from services.gmail_service import GmailService
from utils.email_utils import is_valid_email, normalize_email

class NotificationService:
    """Service for handling employee notifications."""
    
    def __init__(self, gmail_service: Optional[GmailService] = None):
        self.gmail_service = gmail_service or GmailService()
        self.logger = logging.getLogger(__name__)

    def notify_payment(self, employee: Employee, reference_date: date) -> bool:
        """
        Notify an employee about their payment.
        
        Args:
            employee: The employee to notify
            reference_date: The reference date of the payment
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        # Validate email
        if not is_valid_email(employee.email):
            self.logger.warning(
                f"Invalid email for employee {employee.name} ({employee.registration}): {employee.email}"
            )
            return False
            
        # Normalize email
        normalized_email = normalize_email(employee.email)
        
        subject = f"Comprovante de Pagamento - {reference_date.strftime('%m/%Y')}"
        body = self._create_notification_body(employee, reference_date)
        
        # Get both paycheck and payment receipt files
        attachments = self._get_attachments(employee)
        
        if not attachments:
            print(f"ER {employee.name} ({employee.registration}) - Ocorreu um erro - Nenhum anexo encontrado")
            return False
            
        try:
            # Preparar lista de anexos para exibição
            attachment_names = [os.path.basename(attachment) for attachment in attachments]
            attachments_str = " e ".join(attachment_names)
            
            print(f"OK {employee.name} ({employee.registration}) - Email enviado - Anexos: {attachments_str}")
            
            self.gmail_service.send_email(
                 to=normalized_email,
                 subject=subject,
                 body=body,
                 attachments=attachments
            )
            
            return True
            
        except Exception as e:
            print(f"ER {employee.name} ({employee.registration}) - Ocorreu um erro - {str(e)}")
            return False
    
    def _get_attachments(self, employee: Employee) -> list[str]:
        """
        Get attachment files for the employee.
        
        Args:
            employee: The employee to get attachments for
            
        Returns:
            List of valid attachment file paths
        """
        attachments = []
        
        # Check if employee has paycheck
        if not hasattr(employee, 'paycheck') or not employee.paycheck:
            return attachments
            
        if not employee.paycheck.file_path:
            return attachments
            
        # Add contra-cheque
        paycheck_path = employee.paycheck.file_path
        if os.path.exists(paycheck_path) and os.access(paycheck_path, os.R_OK):
            attachments.append(paycheck_path)
            
        # Add payment receipt - same folder as paycheck but with different suffix
        receipt_path = paycheck_path.replace("Contra-Cheque.pdf", "pagamento.pdf")
        if os.path.exists(receipt_path) and os.access(receipt_path, os.R_OK):
            attachments.append(receipt_path)
            
        return attachments
        
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