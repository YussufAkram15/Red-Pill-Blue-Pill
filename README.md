# Secure Vault GUI

A modern, user-friendly GUI application for encrypting and decrypting files using military-grade AES-256-GCM encryption.

## Overview

Secure Vault GUI provides a secure and intuitive interface for protecting sensitive files with advanced cryptographic standards. Built with Python and featuring a sleek matrix-themed design, it combines security with usability.

## Features

- **AES-256-GCM Encryption**: Military-grade encryption standard for maximum security
- **Intuitive GUI**: Clean, modern interface built with CustomTkinter
- **Drag & Drop Support**: Easily select files by dragging and dropping
- **Key Confirmation**: Ensures password accuracy before encryption
- **Background Processing**: Non-blocking operations with status updates
- **Thread-Safe Operations**: Handles encryption/decryption without freezing the UI
- **Error Handling**: Comprehensive validation and user-friendly error messages
- **File Overwrite Protection**: Prompts before overwriting existing files

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`:
  - customtkinter
  - tkinterdnd2
  - cryptography

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YussufAkram15/Red-Pill-Blue-Pill.git
   cd Red-Pill-Blue-Pill
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Application

```bash
python secure_vault_gui.py
```

### Encrypting Files

1. Launch the application
2. Select a file via drag-and-drop or click to browse
3. Enter an encryption key (minimum 4 characters)
4. Confirm the key
5. Click **EXECUTE** to encrypt
6. The encrypted file will be saved with `.enc` extension

### Decrypting Files

1. Launch the application
2. Select an encrypted `.enc` file
3. Switch to **DECRYPT** mode
4. Enter the original encryption key
5. Click **EXECUTE** to decrypt
6. The decrypted file will be saved in the same directory

## Security Considerations

- **Key Strength**: Use strong, random encryption keys (16+ characters recommended)
- **Key Management**: Never share your encryption keys; store them securely
- **File Integrity**: Encrypted files use authenticated encryption (GCM mode) to detect tampering
- **Temporary Data**: Clear sensitive data from memory after operations
- **Virtual Environment**: It's recommended to run this application in a dedicated Python virtual environment

## Technical Details

- **Encryption Algorithm**: AES-256-GCM (Advanced Encryption Standard with 256-bit keys)
- **Key Derivation**: PBKDF2 with SHA-256
- **Architecture**: Multi-threaded GUI with async processing
- **UI Framework**: CustomTkinter (modern tkinter wrapper)

## Project Structure

```
├── secure_vault_gui.py    # Main GUI application
├── vault_crypto.py        # Encryption/decryption logic
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## License

This project is provided as-is for educational and personal use.

## Author

Created by Yussuf Akram

## Disclaimer

This application is provided without warranty. While it uses industry-standard encryption, users are responsible for maintaining secure backups of their encryption keys. Loss of encryption keys will result in permanent data loss.