import tkinter as tk
from tkinter import ttk

class VentasPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.label = ttk.Label(self, text=" 🛒 Welcome to ventas Page", font=("Arial", 18)).pack(pady=20)

