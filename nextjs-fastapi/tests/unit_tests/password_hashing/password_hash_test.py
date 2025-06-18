import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from backend.service.PasswordHashService import PasswordHashService

# Test case for User creation and initialization
def test_hash_password():

    password = "1234"
    hashed_password = PasswordHashService.hash_password(password)

    assert hashed_password != password

    print(hashed_password)

    assert hashed_password.startswith("$argon2id$v=") is True # means its hashed

    assert len(hashed_password) > 40 # hash should be significant

def test_verify_password_true():

    password = "cookie monster"
    hashed_password = PasswordHashService.hash_password(password)

    assert PasswordHashService.verify_password(hashed_password, password) is True


def test_verify_password_false():
    password = "cookie monster"
    hashed_password = PasswordHashService.hash_password(password)

    assert PasswordHashService.verify_password(hashed_password, "cook") is False

