"""Action buttons component."""
import customtkinter as ctk
from typing import Callable

class ActionButtons(ctk.CTkFrame):
    """Component for main action buttons."""
    
    def __init__(
        self,
        master,
        on_process_payroll: Callable[[], None],
        on_process_receipts: Callable[[], None]
    ):
        """Initialize the action buttons."""
        super().__init__(master)
        
        self.on_process_payroll = on_process_payroll
        self.on_process_receipts = on_process_receipts
        
        self._create_widgets()
        self._create_layout()
        
    def _create_widgets(self):
        """Create component widgets."""
        # Process payroll button
        self.process_payroll_btn = ctk.CTkButton(
            self,
            text="Processar Folha",
            command=self.on_process_payroll,
            width=200
        )
        
        # Process receipts button
        self.process_receipts_btn = ctk.CTkButton(
            self,
            text="Processar Comprovantes",
            command=self.on_process_receipts,
            width=200
        )
        
    def _create_layout(self):
        """Create component layout."""
        self.process_payroll_btn.grid(row=0, column=0, padx=10)
        self.process_receipts_btn.grid(row=0, column=1, padx=10)