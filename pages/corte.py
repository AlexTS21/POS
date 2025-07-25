import tkinter as tk
from tkinter import ttk

class CortePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.label = ttk.Label(self, text="Welcome to cote Page", font=("Arial", 18)).pack(pady=20)

