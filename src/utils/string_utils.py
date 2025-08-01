"""Utility functions for string manipulation."""
import unicodedata
import re


def normalize_text(text: str) -> str:
    """
    Remove accents and special characters from text, keeping only alphanumeric and spaces.
    
    Args:
        text: The text to normalize
        
    Returns:
        str: The normalized text containing only alphanumeric characters and spaces
        
    Example:
        >>> normalize_text("João & Maria")
        "Joao Maria"
    """
    # Remove accents
    without_accents = "".join(
        char for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )
    
    # Remove special characters, keeping only alphanumeric and spaces
    return re.sub(r"[^a-zA-Z0-9\s]", "", without_accents)
