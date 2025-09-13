import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20)
        
        header_label = ttk.Label(header_frame, text="Password Generator", style='Header.TLabel')
        header_label.pack()
        
        # Main content frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=10)
        
        # Password length
        length_frame = ttk.Frame(main_frame)
        length_frame.pack(fill='x', pady=10)
        
        length_label = ttk.Label(length_frame, text="Password Length:")
        length_label.pack(side='left')
        
        self.length_var = tk.IntVar(value=12)
        self.length_spinbox = ttk.Spinbox(length_frame, from_=6, to=50, width=5, textvariable=self.length_var)
        self.length_spinbox.pack(side='left', padx=10)
        
        # Character types
        types_frame = ttk.Frame(main_frame)
        types_frame.pack(fill='x', pady=10)
        
        types_label = ttk.Label(types_frame, text="Include:")
        types_label.pack(anchor='w')
        
        self.upper_var = tk.BooleanVar(value=True)
        upper_check = ttk.Checkbutton(types_frame, text="Uppercase Letters", variable=self.upper_var)
        upper_check.pack(anchor='w', pady=2)
        
        self.lower_var = tk.BooleanVar(value=True)
        lower_check = ttk.Checkbutton(types_frame, text="Lowercase Letters", variable=self.lower_var)
        lower_check.pack(anchor='w', pady=2)
        
        self.digits_var = tk.BooleanVar(value=True)
        digits_check = ttk.Checkbutton(types_frame, text="Digits", variable=self.digits_var)
        digits_check.pack(anchor='w', pady=2)
        
        self.symbols_var = tk.BooleanVar(value=True)
        symbols_check = ttk.Checkbutton(types_frame, text="Symbols", variable=self.symbols_var)
        symbols_check.pack(anchor='w', pady=2)
        
        # Generate button
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        generate_btn = ttk.Button(button_frame, text="Generate Password", command=self.generate_password)
        generate_btn.pack()
        
        # Generated password
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill='x', pady=10)
        
        password_label = ttk.Label(password_frame, text="Generated Password:")
        password_label.pack(anchor='w')
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.password_var, font=('Arial', 12), state='readonly')
        password_entry.pack(fill='x', pady=5)
        
        # Copy button
        copy_btn = ttk.Button(password_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.pack(pady=5)
        
        # Strength indicator
        strength_frame = ttk.Frame(main_frame)
        strength_frame.pack(fill='x', pady=10)
        
        strength_label = ttk.Label(strength_frame, text="Password Strength:")
        strength_label.pack(anchor='w')
        
        self.strength_var = tk.StringVar(value="")
        strength_value = ttk.Label(strength_frame, textvariable=self.strength_var, font=('Arial', 10, 'bold'))
        strength_value.pack(anchor='w', pady=2)
        
        self.strength_bar = ttk.Progressbar(strength_frame, length=200, mode='determinate')
        self.strength_bar.pack(fill='x', pady=5)
    
    def generate_password(self):
        # Check if at least one character type is selected
        if not any([self.upper_var.get(), self.lower_var.get(), 
                   self.digits_var.get(), self.symbols_var.get()]):
            messagebox.showerror("Error", "Please select at least one character type.")
            return
        
        # Define character sets
        upper_chars = string.ascii_uppercase if self.upper_var.get() else ''
        lower_chars = string.ascii_lowercase if self.lower_var.get() else ''
        digit_chars = string.digits if self.digits_var.get() else ''
        symbol_chars = string.punctuation if self.symbols_var.get() else ''
        
        # Combine character sets
        all_chars = upper_chars + lower_chars + digit_chars + symbol_chars
        
        # Generate password
        length = self.length_var.get()
        password = ''.join(random.choice(all_chars) for _ in range(length))
        
        # Set password
        self.password_var.set(password)
        
        # Calculate and display strength
        self.calculate_strength(password)
    
    def calculate_strength(self, password):
        length = len(password)
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_lower = any(c in string.ascii_lowercase for c in password)
        has_digit = any(c in string.digits for c in password)
        has_symbol = any(c in string.punctuation for c in password)
        
        # Score calculation
        score = 0
        
        # Length contributes up to 40% of the score
        score += min(40, length * 2)
        
        # Character variety contributes up to 60% of the score
        variety_count = sum([has_upper, has_lower, has_digit, has_symbol])
        score += variety_count * 15
        
        # Set strength text and bar
        if score < 50:
            strength = "Weak"
            color = "red"
        elif score < 80:
            strength = "Medium"
            color = "orange"
        else:
            strength = "Strong"
            color = "green"
        
        self.strength_var.set(f"{strength} ({score}/100)")
        self.strength_bar['value'] = score
        self.strength_bar['style'] = f"Horizontal.TProgressbar.{color.capitalize()}"
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()