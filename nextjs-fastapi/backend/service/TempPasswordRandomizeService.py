import secrets
import string
import random


def create_temp_password() -> str:
    length = random.randrange(8, 16)

    alphabet = string.ascii_letters + string.digits + string.punctuation

    temp_password = ''.join(secrets.choice(alphabet) for i in range(length))

    return temp_password

