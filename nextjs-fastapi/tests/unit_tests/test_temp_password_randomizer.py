import pytest
import string
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from backend.service.TempPasswordRandomizeService import create_temp_password


# Test that the password has the correct length
def test_generate_temp_password_length():
    # Test for default length (12 characters)
    password = create_temp_password()
    assert 8 <= len(password) <= 16, f"Expected password length between 8 and 16, but got {len(password)}"


# Test that the password contains only valid characters
def test_generate_temp_password_characters():
    password = create_temp_password()

    valid_chars = string.ascii_letters + string.digits + string.punctuation
    assert all(char in valid_chars for char in password), f"Password contains invalid characters: {password}"


# Test randomness by generating multiple passwords and making sure they're not the same
def test_generate_temp_password_randomness():
    passwords = {create_temp_password() for _ in range(100)}  # Generate 100 passwords]

    # Check if there's more than one unique password
    assert len(passwords) > 90, "Passwords are not random; many generated passwords are the same."