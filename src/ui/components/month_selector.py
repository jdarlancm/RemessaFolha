"""Month selector component."""
import customtkinter as ctk
from datetime import date
from typing import Optional

from utils.date_utils import nome_mes

class MonthSelector(ctk.CTkFrame):
    """Component for selecting month and year."""
    
    def __init__(self, master):
        """Initialize the month selector."""
        super().__init__(master)
        
        self._create_widgets()
        self._create_layout()
        
    def _create_widgets(self):
        """Create component widgets."""
        # Month combobox
        current_month = date.today().month
        months = [(i, nome_mes(i)) for i in range(1, 13)]
        
        self.month_label = ctk.CTkLabel(self, text="Mês:")
        self.month_combo = ctk.CTkComboBox(
            self,
            values=[month[1] for month in months],
            width=200
        )
        self.month_combo.set(nome_mes(current_month))
        
        # Year entry
        current_year = date.today().year
        self.year_label = ctk.CTkLabel(self, text="Ano:")
        self.year_entry = ctk.CTkEntry(self, width=100)
        self.year_entry.insert(0, str(current_year))
        
    def _create_layout(self):
        """Create component layout."""
        self.month_label.grid(row=0, column=0, padx=5)
        self.month_combo.grid(row=0, column=1, padx=5)
        self.year_label.grid(row=0, column=2, padx=5)
        self.year_entry.grid(row=0, column=3, padx=5)
        
    def get_selected_date(self) -> Optional[date]:
        """Get the selected date."""
        try:
            # Get month number from name
            month_name = self.month_combo.get()
            for i in range(1, 13):
                if nome_mes(i) == month_name:
                    month = i
                    break
            else:
                return None
                
            # Get year
            year = int(self.year_entry.get())
            
            return date(year, month, 1)
        except (ValueError, TypeError):
            return None