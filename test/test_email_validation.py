"""Tests for email validation functionality."""
import pytest
from src.utils.email_utils import is_valid_email, normalize_email

class TestEmailValidation:
  """Test cases for email validation."""
  
  def test_valid_emails(self):
    """Test valid email addresses."""
    valid_emails = [
      "user@example.com",
      "test.email@domain.org",
      "user+tag@example.co.uk",
      "firstname.lastname@company.com.br",
      "123@test.com"
    ]
    
    for email in valid_emails:
      assert is_valid_email(email), f"Email should be valid: {email}"
      
  def test_invalid_emails(self):
    """Test invalid email addresses."""
    invalid_emails = [
      None,
      "",
      "   ",
      "invalid-email",
      "@domain.com",
      "user@",
      "user@domain",
      "user..double.dot@domain.com",
      "user@domain..com",
      "nan",
      "null",
      "none",
      "n/a"
    ]
    
    for email in invalid_emails:
      assert not is_valid_email(email), f"Email should be invalid: {email}"
      
  def test_normalize_email(self):
    """Test email normalization."""
    test_cases = [
      ("  USER@EXAMPLE.COM  ", "user@example.com"),
      ("Test.Email@Domain.Org", "test.email@domain.org"),
      ("", None),
      ("nan", None),
      ("invalid-email", None)
    ]
    
    for input_email, expected in test_cases:
      result = normalize_email(input_email)
      assert result == expected, f"Normalization failed for {input_email}"
