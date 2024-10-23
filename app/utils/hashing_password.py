import hashlib

default_salt = "peep_backend"


def hash_password(password: str, salt: str = default_salt) -> str:
    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return pw_hash.hex()


def is_correct_password(pw_hash: str, password: str, salt: str = default_salt) -> bool:
    hash_for_check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    return pw_hash == hash_for_check
