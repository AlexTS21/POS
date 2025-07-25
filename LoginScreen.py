import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import sqlite3


class LoginScreen:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success #Recive data
        self.style = ttkb.Style(theme="minty")
        
        # Set window to fullscreen
        #self.root.attributes('-fullscreen', True)
        
        # Alternatively, if you just want maximized:
        self.root.state('zoomed')
        
        self.setup_login_ui()
    
    def setup_login_ui(self):
        """Create the login interface"""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title("Login")
        
        
        # Create a container frame that will center its contents
        container = ttk.Frame(self.root)
        container.pack(expand=True, fill='both')
        
        # Main frame with fixed size that will be centered
        self.login_frame = ttk.Frame(container, width=400, height=350, padding=20)
        self.login_frame.pack(expand=True)
        self.login_frame.pack_propagate(False)  # Prevent frame from shrinking to fit contents
        
        # Header
        ttk.Label(
            self.login_frame, 
            text="Introduce tus credenciales \nde acceso", 
            font=('Helvetica', 16, 'bold'),
            anchor="center",  # Centers the text within the label's space
            justify="center"  # Centers each line of multi-line text
        ).pack(pady=10)
        
        # Username field
        ttk.Label(self.login_frame, text="Usuario:").pack(pady=(10, 0))
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack(fill='x', pady=5)
        self.username_entry.focus()
        
        # Password field
        ttk.Label(self.login_frame, text="Contraseña:").pack(pady=(10, 0))
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.pack(fill='x', pady=5)
        
        # Login button
        login_btn = ttk.Button(
            self.login_frame,
            text="Acceder",
            command=self.attempt_login,
            bootstyle=PRIMARY
        )
        login_btn.pack(pady=20)
        
        # Error label (hidden by default)
        self.error_label = ttk.Label(
            self.login_frame,
            text="",
            bootstyle=DANGER,
            wraplength=350
        )
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.attempt_login())
        
        # Add escape key to exit fullscreen
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
    
    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.check_credentials(username, password)
        if user:
            self.error_label.pack_forget()
            self.root.attributes('-fullscreen', False)
            self.login_frame.destroy()
            self.on_login_success(user)  # Pass user data to MainApplication
        else:
            self.error_label.config(text="Usuario o contraseña incorrectos")
            self.error_label.pack()

    def check_credentials(self, username, password):
        try:
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            cur.execute("SELECT id, username, fullname, type FROM users WHERE username=? AND password=? AND active=1", (username, password))
            user = cur.fetchone()
            conn.close()
            if user:
                return {
                    "id": user[0],
                    "username": user[1],
                    "fullname": user[2],
                    "type": user[-1]
                    
                }
            return None
        except Exception as e:
            print("DB error:", e)
            return None
        finally:
            conn.close()  # Ensure cleanup
