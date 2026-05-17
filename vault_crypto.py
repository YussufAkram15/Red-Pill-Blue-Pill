"""
Cryptographic operations for Secure Vault.
Handles AES-GCM encryption/decryption with PBKDF2 key derivation.
"""

import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Encryption constants
MAGIC = b"SVAULT01"
SALT_SIZE = 32
IV_SIZE = 12
TAG_SIZE = 16
KEY_SIZE = 32
PBKDF2_ITERS = 600_000


def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive an encryption key from password and salt using PBKDF2-SHA256.
    
    Args:
        password: User's password string
        salt: Random salt bytes for key derivation
        
    Returns:
        32-byte encryption key
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=PBKDF2_ITERS,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt_file(input_path: str, output_path: str, password: str) -> None:
    """
    Encrypt a file using AES-256-GCM.
    
    Args:
        input_path: Path to file to encrypt
        output_path: Path to write encrypted file
        password: Encryption password
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        IOError: If file operations fail
    """
    # Generate random salt and IV
    salt = os.urandom(SALT_SIZE)
    iv = os.urandom(IV_SIZE)
    
    # Derive key from password
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    
    # Read plaintext
    with open(input_path, "rb") as f:
        plaintext = f.read()
    
    # Encrypt
    ciphertext_with_tag = aesgcm.encrypt(iv, plaintext, None)
    
    # Write: MAGIC + SALT + IV + CIPHERTEXT+TAG
    with open(output_path, "wb") as f:
        f.write(MAGIC + salt + iv + ciphertext_with_tag)


def decrypt_file(input_path: str, output_path: str, password: str) -> None:
    """
    Decrypt a file encrypted with encrypt_file().
    
    Args:
        input_path: Path to encrypted file
        output_path: Path to write decrypted file
        password: Decryption password
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If file format is invalid or password is wrong
        IOError: If file operations fail
    """
    with open(input_path, "rb") as f:
        # Read and validate magic number
        magic = f.read(len(MAGIC))
        if magic != MAGIC:
            raise ValueError("Invalid file format: not a Secure Vault encrypted file")
        
        # Read salt and IV
        salt = f.read(SALT_SIZE)
        iv = f.read(IV_SIZE)
        
        # Read ciphertext with tag
        ciphertext_with_tag = f.read()
    
    if len(ciphertext_with_tag) < TAG_SIZE:
        raise ValueError("File corrupted: incomplete ciphertext")
    
    # Derive key and decrypt
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    
    try:
        plaintext = aesgcm.decrypt(iv, ciphertext_with_tag, None)
    except Exception as e:
        raise ValueError("Decryption failed: invalid password or corrupted file") from e
    
    # Write plaintext
    with open(output_path, "wb") as f:
        f.write(plaintext)
