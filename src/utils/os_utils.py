"""Utility functions for operating system operations."""
import os
from typing import List, Optional


def is_exist_path(path: str) -> bool:
    """
    Check if a directory path exists.
    
    Args:
        path: The directory path to check
        
    Returns:
        bool: True if the path exists and is a directory
    """
    return os.path.exists(path) and os.path.isdir(path)


def is_exist_file(full_path_filename: str) -> bool:
    """
    Check if a file exists.
    
    Args:
        full_path_filename: The complete path to the file
        
    Returns:
        bool: True if the file exists
    """
    return os.path.exists(full_path_filename) and os.path.isfile(full_path_filename)


def create_path_if_not_exits(path: str) -> None:
    """
    Create a directory if it doesn't exist.
    
    Args:
        path: The directory path to create
    """
    if not is_exist_path(path):
        os.makedirs(path)


def get_environment_variable(variable: str) -> Optional[str]:
    """
    Get the value of an environment variable.
    
    Args:
        variable: The name of the environment variable
        
    Returns:
        Optional[str]: The value of the environment variable, or None if not set
    """
    return os.getenv(variable)


def list_files(path: str, filter_extension: Optional[str] = None) -> List[str]:
    """
    List files in a directory, optionally filtered by extension.
    
    Args:
        path: The directory path to list files from
        filter_extension: Optional file extension to filter by (e.g. '.pdf')
        
    Returns:
        List[str]: List of filenames in the directory
    """
    files = os.listdir(path)
    if filter_extension:
        return [f for f in files if f.endswith(filter_extension)]
    return files
