import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
from PIL import Image, ImageTk


class PasswordGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Password Generator")

        # Set a fixed size instead of fullscreen
        master.geometry("600x700")
        master.resizable(False, False)

        # Color scheme
        self.bg_color = "#F0F4F8"  # Light grayish blue
        self.fg_color = "#1A202C"  # Dark gray
        self.accent_color = "#3182CE"  # Blue
        self.button_color = "#48BB78"  # Green

        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure colors and fonts
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color, font=('Arial', 12))
        self.style.configure('TCheckbutton', background=self.bg_color, foreground=self.fg_color, font=('Arial', 12))
        self.style.map('TCheckbutton', background=[('active', self.bg_color)])  # Fix hover issue
        self.style.configure('TButton', background=self.button_color, foreground='white', font=('Arial', 12, 'bold'))
        self.style.map('TButton', background=[('active', self.accent_color)])

        self.main_frame = ttk.Frame(self.master, style='TFrame')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        self.create_widgets()

    def create_widgets(self):
        # Logo
        self.logo_image = Image.open("logo.png")  # Make sure to have this image in the same directory
        self.logo_image = self.logo_image.resize((150, 150), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        logo_label = ttk.Label(self.main_frame, image=self.logo_photo, background=self.bg_color)
        logo_label.pack(pady=(0, 20))

        # Title
        title_label = ttk.Label(self.main_frame, text="MyPass Generator", font=('Arial', 24, 'bold'),
                                foreground=self.accent_color)
        title_label.pack(pady=(0, 30))

        # Password Length
        length_frame = ttk.Frame(self.main_frame, style='TFrame')
        length_frame.pack(fill='x', pady=10)
        ttk.Label(length_frame, text="Password Length:").pack(side='left', padx=(0, 10))
        self.length_var = tk.IntVar(value=12)
        length_spinbox = ttk.Spinbox(length_frame, from_=8, to=50, textvariable=self.length_var, width=5)
        length_spinbox.pack(side='left')

        # Character Types
        types_frame = ttk.Frame(self.main_frame, style='TFrame')
        types_frame.pack(fill='x', pady=10)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        ttk.Checkbutton(types_frame, text="Uppercase", variable=self.use_uppercase,
                        command=self.update_char_types).pack(side='left', padx=(0, 20))
        ttk.Checkbutton(types_frame, text="Lowercase", variable=self.use_lowercase,
                        command=self.update_char_types).pack(side='left', padx=(0, 20))
        ttk.Checkbutton(types_frame, text="Digits", variable=self.use_digits, command=self.update_char_types).pack(
            side='left', padx=(0, 20))
        ttk.Checkbutton(types_frame, text="Symbols", variable=self.use_symbols, command=self.update_char_types).pack(
            side='left')

        # Exclude Characters
        exclude_frame = ttk.Frame(self.main_frame, style='TFrame')
        exclude_frame.pack(fill='x', pady=10)
        ttk.Label(exclude_frame, text="Exclude Characters:").pack(side='left', padx=(0, 10))
        self.exclude_chars = tk.StringVar()
        exclude_entry = ttk.Entry(exclude_frame, textvariable=self.exclude_chars, width=30)
        exclude_entry.pack(side='left')

        # Generate Button
        generate_button = ttk.Button(self.main_frame, text="Generate Password", command=self.generate_password)
        generate_button.pack(pady=30)

        # Password Display
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(self.main_frame, textvariable=self.password_var, width=40,
                                   font=('Arial', 14, 'bold'))
        password_entry.pack(pady=10)
        password_entry.config(state='readonly')

        # Password Strength
        self.strength_var = tk.StringVar(value="Strength: N/A")
        self.strength_label = ttk.Label(self.main_frame, textvariable=self.strength_var, font=('Arial', 12, 'bold'))
        self.strength_label.pack(pady=10)

        # Copy to Clipboard Button
        copy_button = ttk.Button(self.main_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_button.pack(pady=10)

    def update_char_types(self):
        if not any([self.use_uppercase.get(), self.use_lowercase.get(), self.use_digits.get(), self.use_symbols.get()]):
            messagebox.showwarning("Warning", "At least one character type must be selected.")
            last_unchecked = \
            [var for var in [self.use_uppercase, self.use_lowercase, self.use_digits, self.use_symbols] if
             not var.get()][0]
            last_unchecked.set(True)

    def generate_password(self):
        length = self.length_var.get()
        chars = ""

        if self.use_uppercase.get():
            chars += string.ascii_uppercase
        if self.use_lowercase.get():
            chars += string.ascii_lowercase
        if self.use_digits.get():
            chars += string.digits
        if self.use_symbols.get():
            chars += string.punctuation

        exclude = self.exclude_chars.get()
        chars = ''.join(ch for ch in chars if ch not in exclude)

        if not chars:
            messagebox.showerror("Error", "No character set selected!")
            return

        password = ''.join(random.choice(chars) for _ in range(length))

        while not (
                (not self.use_uppercase.get() or any(c.isupper() for c in password)) and
                (not self.use_lowercase.get() or any(c.islower() for c in password)) and
                (not self.use_digits.get() or any(c.isdigit() for c in password)) and
                (not self.use_symbols.get() or any(c in string.punctuation for c in password))
        ):
            password = ''.join(random.choice(chars) for _ in range(length))

        self.password_var.set(password)
        self.evaluate_strength(password)

    def evaluate_strength(self, password):
        length = len(password)
        strength = "Weak"

        if length >= 12 and (any(c.islower() for c in password) and
                             any(c.isupper() for c in password) and
                             any(c.isdigit() for c in password) and
                             any(c in string.punctuation for c in password)):
            strength = "Strong"
            color = self.button_color
        elif length >= 8 and ((any(c.islower() for c in password) and any(c.isupper() for c in password)) or
                              (any(c.isdigit() for c in password) and any(c in string.punctuation for c in password))):
            strength = "Medium"
            color = self.accent_color
        else:
            color = "red"

        self.strength_var.set(f"Strength: {strength}")
        self.strength_label.config(foreground=color)

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
            self.password_var.set("")  # Clear password after copying
        else:
            messagebox.showwarning("Warning", "No password to copy!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

