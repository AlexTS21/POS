import tkinter as tk
from tkinter import ttk

class ConfiguracionPage(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)

        # Alinear arriba a la izquierda con margen
        ttk.Label(self, text="Settings", font=('Helvetica', 24)).pack(anchor='nw', padx=10, pady=10)

        form_frame = ttk.Frame(self)
        form_frame.pack(anchor='nw', padx=10)

        ttk.Label(form_frame, text="Theme:").grid(row=0, column=0, padx=5, pady=5, sticky='e')

        themes = style.theme_names()
        theme_var = tk.StringVar(value=style.theme_use())

        ttk.OptionMenu(
            form_frame, theme_var, theme_var.get(),
            *themes, command=lambda t: style.theme_use(t)
        ).grid(row=0, column=1, padx=5, pady=5, sticky='w')
