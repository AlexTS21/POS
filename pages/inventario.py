import tkinter as tk
from tkinter import ttk

class InventarioPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.label = ttk.Label(self, text="Welcome to inventario Page", font=("Arial", 18)).pack(pady=20)

