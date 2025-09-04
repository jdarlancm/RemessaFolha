"""Main application window for RemessaFolha."""
import sys
from pathlib import Path

# Adicionar src ao PYTHONPATH
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

import customtkinter as ctk
from datetime import date

from ui.windows.main_window import MainWindow

class RemessaFolhaApp:
    """Main application class."""
    
    def __init__(self):
        """Initialize the application."""
        # Set appearance mode and default theme
        ctk.set_appearance_mode("system")  # default is system setting
        ctk.set_default_color_theme("blue")  # themes: blue (default), dark-blue, green
        
        # Create main window
        self.window = MainWindow()
        
    def run(self):
        """Run the application."""
        self.window.mainloop()

def main():
    """Application entry point."""
    app = RemessaFolhaApp()
    app.run()

if __name__ == "__main__":
    main()