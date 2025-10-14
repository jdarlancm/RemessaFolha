"""Email validation utilities."""
import re
from typing import Optional

def is_valid_email(email: Optional[str]) -> bool:
  """
  Validate if an email address is properly formatted.
  
  Args:
    email: Email address to validate
      
  Returns:
    True if email is valid, False otherwise
  """
  if not email:
    return False
    
  # Remove whitespace
  email = email.strip()
  
  # Check for common invalid values
  invalid_values = ["nan", "null", "none", "", "n/a", "na"]
  if email.lower() in invalid_values:
    return False
    
  # Basic email regex pattern
  email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
  
  if not re.match(email_pattern, email):
    return False
    
  # Additional checks
  if len(email) > 254:  # RFC 5321 limit
    return False
    
  if email.count('@') != 1:
    return False
    
  return True

def normalize_email(email: Optional[str]) -> Optional[str]:
  """
  Normalize email address by trimming whitespace and converting to lowercase.
  
  Args:
    email: Email address to normalize
      
  Returns:
    Normalized email or None if invalid
  """
  if not email:
    return None
    
  email = email.strip().lower()
  
  if not is_valid_email(email):
    return None
    
  return email
