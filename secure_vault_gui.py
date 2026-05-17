"""
Secure Vault GUI - AES-256-GCM File Encryption Application
A modern GUI for encrypting and decrypting files with military-grade security.
"""
from pathlib import Path
from threading import Thread
from tkinter import messagebox, filedialog
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

# Import crypto module
from vault_crypto import encrypt_file, decrypt_file

# --- THEME CONSTANTS ---
GREEN = "#00FF41"  # Classic Matrix Green
DARK_BG = "#000000"
ACCENT = "#003B00"

class SecureVaultGUI(ctk.CTk, TkinterDnD.DnDWrapper):
    """Main application window for Secure Vault encryption/decryption."""
    
    def __init__(self) -> None:
        """Initialize the GUI application."""
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        
        # Window Setup
        self.title("Red Pill / Blue Pill")
        self.geometry("600x650")
        self.configure(fg_color=DARK_BG)
        self.resizable(False, False)
        
        # UI State
        self.selected_file: Path | None = None
        self.mode = ctk.StringVar(value="encrypt")
        self.is_processing = False

        self.setup_ui()

    def setup_ui(self) -> None:
        """Build the user interface."""
        # Header
        self.header = ctk.CTkLabel(
            self, text="[ Red Pill / Blue Pill ]", 
            font=("Courier", 24, "bold"), text_color=GREEN
        )
        self.header.pack(pady=20)

        # Drag and Drop Zone
        self.drop_frame = ctk.CTkFrame(
            self, width=500, height=150, 
            fg_color=ACCENT, border_color=GREEN, border_width=2
        )
        self.drop_frame.pack(pady=10, padx=20)
        self.drop_frame.pack_propagate(False)

        self.drop_label = ctk.CTkLabel(
            self.drop_frame, text="DROP FILE HERE OR CLICK TO SELECT",
            font=("Courier", 14), text_color=GREEN
        )
        self.drop_label.pack(expand=True)

        # Register Drag and Drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.handle_drop)
        self.drop_frame.bind("<Button-1>", lambda e: self.select_file_manual())

        # Password Section
        self.pass_label = ctk.CTkLabel(
            self, text="ENTER ENCRYPTION KEY:", 
            font=("Courier", 12), text_color=GREEN
        )
        self.pass_label.pack(pady=(20, 0))
        
        self.password_entry = ctk.CTkEntry(
            self, show="*", width=300, fg_color="#111", 
            border_color=GREEN, text_color=GREEN, font=("Courier", 14)
        )
        self.password_entry.pack(pady=5)

        # Confirm Password (only for encryption)
        self.confirm_pass_label = ctk.CTkLabel(
            self, text="CONFIRM KEY (ENCRYPT ONLY):", 
            font=("Courier", 12), text_color=GREEN
        )
        self.confirm_pass_label.pack(pady=(10, 0))
        
        self.confirm_password_entry = ctk.CTkEntry(
            self, show="*", width=300, fg_color="#111", 
            border_color=GREEN, text_color=GREEN, font=("Courier", 14)
        )
        self.confirm_password_entry.pack(pady=5)

        # Mode Selection
        self.radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.radio_frame.pack(pady=15)
        
        self.enc_radio = ctk.CTkRadioButton(
            self.radio_frame, text="ENCRYPT", variable=self.mode, value="encrypt",
            command=self.update_password_visibility,
            border_color=GREEN, hover_color=GREEN, text_color=GREEN, font=("Courier", 12)
        )
        self.enc_radio.pack(side="left", padx=20)

        self.dec_radio = ctk.CTkRadioButton(
            self.radio_frame, text="DECRYPT", variable=self.mode, value="decrypt",
            command=self.update_password_visibility,
            border_color=GREEN, hover_color=GREEN, text_color=GREEN, font=("Courier", 12)
        )
        self.dec_radio.pack(side="left", padx=20)

        # Execute Button
        self.exec_button = ctk.CTkButton(
            self, text="EXECUTE", command=self.process,
            fg_color=GREEN, text_color=DARK_BG, font=("Courier", 16, "bold"),
            hover_color="#00CC33"
        )
        self.exec_button.pack(pady=20)

        # Status Label
        self.status_label = ctk.CTkLabel(
            self, text="Ready", font=("Courier", 11), text_color="#CCCCCC"
        )
        self.status_label.pack(pady=5)

    def update_password_visibility(self) -> None:
        """Show/hide password confirmation field based on mode."""
        if self.mode.get() == "encrypt":
            self.confirm_pass_label.pack(pady=(10, 0))
            self.confirm_password_entry.pack(pady=5)
        else:
            self.confirm_pass_label.pack_forget()
            self.confirm_password_entry.pack_forget()

    def handle_drop(self, event) -> None:
        """Handle drag-and-drop file selection."""
        file_path = event.data.strip('{}')
        self.set_file(file_path)

    def select_file_manual(self) -> None:
        """Handle manual file selection."""
        file_types = [("Encrypted Files", "*.enc"), ("All Files", "*.*")]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.set_file(file_path)

    def set_file(self, path: str) -> None:
        """Set the selected file and update UI."""
        try:
            self.selected_file = Path(path)
            if not self.selected_file.exists():
                messagebox.showerror("ERROR", f"File not found: {path}")
                self.selected_file = None
                self.drop_label.configure(text="DROP FILE HERE OR CLICK TO SELECT", text_color=GREEN)
                return
            
            self.drop_label.configure(
                text=f"SELECTED: {self.selected_file.name}", 
                text_color="#FFF"
            )
        except Exception as e:
            messagebox.showerror("ERROR", f"Invalid file path: {str(e)}")
            self.selected_file = None

    def validate_inputs(self) -> bool:
        """Validate user inputs before processing."""
        if not self.selected_file:
            messagebox.showerror("ERROR", "Please select a file")
            return False
        
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("ERROR", "Please enter an encryption key")
            return False
        
        if len(password) < 4:
            messagebox.showerror("ERROR", "Key must be at least 4 characters")
            return False
        
        # For encryption, confirm password matches
        if self.mode.get() == "encrypt":
            confirm = self.confirm_password_entry.get()
            if password != confirm:
                messagebox.showerror("ERROR", "Passwords do not match")
                return False
        
        return True

    def process(self) -> None:
        """Process encryption/decryption in a separate thread."""
        if not self.validate_inputs():
            return
        
        if self.is_processing:
            messagebox.showwarning("WARNING", "Operation already in progress")
            return
        
        # Disable UI during processing
        self.is_processing = True
        self.exec_button.configure(state="disabled")
        password = self.password_entry.get()
        
        # Run in background thread
        thread = Thread(
            target=self._process_file, 
            args=(password,), 
            daemon=True
        )
        thread.start()

    def _process_file(self, password: str) -> None:
        """Execute encryption or decryption (runs in background thread)."""
        try:
            self.update_status("Processing... Please wait")
            
            if self.mode.get() == "encrypt":
                self._run_encryption(password)
                self.update_status("Encryption complete")
                messagebox.showinfo(
                    "SUCCESS", 
                    f"File encrypted successfully!\n\n"
                    f"Output: {self.selected_file.parent / (self.selected_file.name + '.enc')}"
                )
            else:
                self._run_decryption(password)
                self.update_status("Decryption complete")
                messagebox.showinfo(
                    "SUCCESS", 
                    f"File decrypted successfully!\n\n"
                    f"Output: {self.selected_file.parent}"
                )
        
        except ValueError as e:
            self.update_status("Operation failed")
            messagebox.showerror("DECRYPTION FAILED", str(e))
        except FileNotFoundError as e:
            self.update_status("File error")
            messagebox.showerror("FILE ERROR", f"File not found: {str(e)}")
        except IOError as e:
            self.update_status("IO error")
            messagebox.showerror("IO ERROR", f"Cannot read/write file: {str(e)}")
        except Exception as e:
            self.update_status("Unexpected error")
            messagebox.showerror("ERROR", f"Unexpected error: {str(e)}")
        finally:
            # Re-enable UI
            self.is_processing = False
            self.exec_button.configure(state="normal")
            self.clear_passwords()

    def _run_encryption(self, password: str) -> None:
        """Perform file encryption."""
        output_path = self.selected_file.with_suffix(self.selected_file.suffix + ".enc")
        
        # Warn if output exists
        if output_path.exists():
            response = messagebox.askyesno(
                "FILE EXISTS",
                f"Output file exists. Overwrite?\n{output_path.name}"
            )
            if not response:
                raise IOError("Encryption cancelled")
        
        encrypt_file(str(self.selected_file), str(output_path), password)

    def _run_decryption(self, password: str) -> None:
        """Perform file decryption."""
        # Determine output path
        if self.selected_file.suffix == ".enc":
            output_path = self.selected_file.with_suffix("")
        else:
            output_path = self.selected_file.with_stem(self.selected_file.stem + "_decrypted")
        
        # Warn if output exists
        if output_path.exists():
            response = messagebox.askyesno(
                "FILE EXISTS",
                f"Output file exists. Overwrite?\n{output_path.name}"
            )
            if not response:
                raise IOError("Decryption cancelled")
        
        decrypt_file(str(self.selected_file), str(output_path), password)

    def update_status(self, message: str) -> None:
        """Update status label safely from threads."""
        self.status_label.configure(text=message)

    def clear_passwords(self) -> None:
        """Clear password fields from memory."""
        self.password_entry.delete(0, "end")
        self.confirm_password_entry.delete(0, "end")

if __name__ == "__main__":
    try:
        app = SecureVaultGUI()
        app.mainloop()
    except ImportError as e:
        print(f"Error: Missing required package - {e}")
        print("Please run: pip install -r requirements.txt")
    except Exception as e:
        print(f"Fatal error: {e}")