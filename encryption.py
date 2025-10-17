import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64

SALT_PATH = "data/salt.bin"

def _get_salt() -> bytes:
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(SALT_PATH):
        # 16 bytes is fine for a PBKDF2 salt
        with open(SALT_PATH, "wb") as f:
            f.write(os.urandom(16))
    with open(SALT_PATH, "rb") as f:
        return f.read()

def derive_key(master_password: str) -> bytes:
    """
    Derive a 32-byte key from the master password using PBKDF2.
    The derived key is then urlsafe-base64-encoded for Fernet.
    """
    salt = _get_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,  # modern recommended range
    )
    key = kdf.derive(master_password.encode("utf-8"))
    return base64.urlsafe_b64encode(key)

def get_fernet(master_password: str) -> Fernet:
    """
    Create a Fernet instance using a key derived from the master password.
    """
    key = derive_key(master_password)
    return Fernet(key)
