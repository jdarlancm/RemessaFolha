"""Main window of the application."""
import customtkinter as ctk
from datetime import date
from typing import Optional

from services.payroll_service import PayrollService
from services.notification_service import NotificationService
from repositories.payroll_repository import PayrollRepository
from ui.components.month_selector import MonthSelector
from ui.components.action_buttons import ActionButtons

class MainWindow(ctk.CTk):
    """Main window class."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Configure window
        self.title("Remessa Folha")
        self.geometry("800x600")
        
        # Initialize services
        self.payroll_repository = PayrollRepository()
        self.notification_service = NotificationService()
        self.payroll_service = PayrollService(
            payroll_repository=self.payroll_repository,
            notification_service=self.notification_service
        )
        
        # Create UI components
        self._create_widgets()
        self._create_layout()
        
    def _create_widgets(self):
        """Create window widgets."""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="Remessa Folha",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        
        # Month selector
        self.month_selector = MonthSelector(self)
        
        # Unified paycheck checkbox
        self.unified_check = ctk.CTkCheckBox(
            self,
            text="Contracheque em arquivo único",
            onvalue=True,
            offvalue=False
        )
        self.unified_check.select()  # Marcado por padrão
        
        # Action buttons
        self.action_buttons = ActionButtons(
            self,
            on_process_payroll=self._on_process_payroll,
            on_process_receipts=self._on_process_receipts
        )
        
        # Status area
        self.status_text = ctk.CTkTextbox(
            self,
            height=200,
            width=600,
            state="disabled"
        )
        
    def _create_layout(self):
        """Create window layout."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # Place widgets
        self.title_label.grid(row=0, column=0, pady=20)
        self.month_selector.grid(row=1, column=0, pady=20)
        self.unified_check.grid(row=2, column=0, pady=10)
        self.action_buttons.grid(row=3, column=0, pady=20)
        self.status_text.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")
        
    def _on_process_payroll(self):
        """Handle process payroll button click."""
        selected_date = self.month_selector.get_selected_date()
        if not selected_date:
            self._show_error("Selecione um mês válido!")
            return
            
        try:
            self._show_message("Processando folha...")
            self.payroll_service.create_remittance(
                reference_date=selected_date,
                unified_paycheck=self.unified_check.get()
            )
            self._show_success("Folha processada com sucesso!")
        except Exception as e:
            self._show_error(f"Erro ao processar folha: {str(e)}")
            
    def _on_process_receipts(self):
        """Handle process receipts button click."""
        selected_date = self.month_selector.get_selected_date()
        if not selected_date:
            self._show_error("Selecione um mês válido!")
            return
            
        try:
            self.payroll_service.process_payment_receipts(selected_date)
            self._show_success("Comprovantes processados com sucesso!")
        except Exception as e:
            self._show_error(f"Erro ao processar comprovantes: {str(e)}")
            
    def _show_message(self, message: str):
        """Show a message in the status area."""
        self.status_text.configure(state="normal")
        self.status_text.insert("end", f"{message}\n")
        self.status_text.see("end")
        self.status_text.configure(state="disabled")
        
    def _show_error(self, message: str):
        """Show an error message."""
        self._show_message(f"ERRO: {message}")
        
    def _show_success(self, message: str):
        """Show a success message."""
        self._show_message(f"SUCESSO: {message}")