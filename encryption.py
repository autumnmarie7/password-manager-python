# --- Imports ---
# os: file operations and generating random bytes
# hashes, PBKDF2HMAc: derive a secure key from the master password
# Fernet: handles encryption/decryption using AES (built-in)
# base64: converts binary key data to text format required by Fernet
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64

SALT_PATH = "data/salt.bin"
# ^ path to store the random salt used for key derivation
# the salt makes each derived key unique, even for identical passwords

def _get_salt() -> bytes:
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(SALT_PATH): # - if no salt file exists, generates a new 16-byte random salt and saves it
        with open(SALT_PATH, "wb") as f:
            f.write(os.urandom(16))
            # 16 bytes is fine for a PBKDF2 salt
    with open(SALT_PATH, "rb") as f:
        return f.read() # - returns the salt bytes
# ^ in summary: retrieves the salt used for key derivation
# this salt is reused every time the app runs - meaning as long as the same master password is used, the same derived key will be produced
# why it matters: if salt changed each time, you wouldn't be able to decrypt old passwords because derived key would change
# it's generated once and stored safely

def derive_key(master_password: str) -> bytes:
     """
    Stretch the user's master password into a strong 32-byte key using PBKDF2-HMAC-SHA256.
    - The salt ensures uniqueness.
    - 390,000 iterations slow down brute-force attempts.
    - The result is base64-encoded for Fernet compatibility.
    """
    salt = _get_salt() # fetches your salt
    kdf = PBKDF2HMAC( #uses this to stretch your master password into a strong cryptographic key
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,  # modern recommended range
    )
    key = kdf.derive(master_password.encode("utf-8"))
    return base64.urlsafe_b64encode(key) # base64-encodes it to make it compatible with Fernet (which expects url-safe base64 keys)

def get_fernet(master_password: str) -> Fernet:
    """
    Build and return a Fernet object for encrypting and decrypting data.
    The Fernet key is securely derived from the master password using PBKDF2.
    """
    key = derive_key(master_password) #securely generates the encryption key from the master password
    return Fernet(key) # passes the key into Fernet, returning a ready-to-use encryption/decryption object
