"""Logging configuration for the application."""
import logging
import os
from datetime import datetime

def setup_logging():
  """Setup logging configuration for the application."""
  
  # Create logs directory if it doesn't exist
  log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
  os.makedirs(log_dir, exist_ok=True)
  
  # Create timestamped log file
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  log_file = os.path.join(log_dir, f"remessa_folha_{timestamp}.log")
  
  # Configure logging
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
      logging.FileHandler(log_file, encoding='utf-8'),
      logging.StreamHandler()  # Also log to console
    ]
  )
  
  # Set specific loggers to appropriate levels
  logging.getLogger('googleapiclient').setLevel(logging.WARNING)
  logging.getLogger('google_auth_oauthlib').setLevel(logging.WARNING)
  
  return log_file
