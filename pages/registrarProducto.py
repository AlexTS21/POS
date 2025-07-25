import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import sqlite3
from ttkbootstrap import Style
import random

class RegistroProductoPage(ttkb.Frame):
    def __init__(self, parent, go_back_callback):
        super().__init__(parent)

        ttkb.Label(self, text="➕ Registrar nuevo producto", font=("Helvetica", 20, "bold"), bootstyle="primary").pack(anchor='nw', padx=30, pady=10)

        form_frame = ttkb.Frame(self)
        form_frame.pack(padx=30, pady=10, fill='x')

        labels = ["Código", "Nombre del producto", "Precio", "Cantidad"]
        self.entries = {}
        self.generate_var = ttkb.IntVar()

        for i, label in enumerate(labels):
            ttkb.Label(form_frame, text=label + ":", font=("Helvetica", 12)).grid(row=i, column=0, sticky="w", pady=5)

            entry = ttkb.Entry(form_frame, font=("Helvetica", 12))
            entry.grid(row=i, column=1, sticky="ew", pady=5)
            self.entries[label.lower()] = entry

            # Si es el campo Código, agregamos el checkbox "Generar"
            if label == "Código":
                generar_checkbox = ttkb.Checkbutton(
                    form_frame,
                    text="Generar",
                    variable=self.generate_var,
                    command=self.toggle_codigo_entry,
                    bootstyle="info"
                )
                generar_checkbox.grid(row=i, column=2, padx=10)

        form_frame.grid_columnconfigure(1, weight=1)

        button_frame = ttkb.Frame(self)
        button_frame.pack(pady=15)

        ttkb.Button(button_frame, text="Registrar producto", bootstyle="success").pack(side="left", padx=10)
        ttkb.Button(button_frame, text="Volver al inventario", bootstyle="secondary", command=go_back_callback).pack(side="left", padx=10)

    def toggle_codigo_entry(self):
        entry = self.entries["código"]
        if self.generate_var.get() == 1:
            random_code = ''.join(str(random.randint(0, 9)) for _ in range(12))
            entry.delete(0, 'end')
            entry.insert(0, random_code)
            entry.config(state='disabled')
        else:
            entry.config(state='normal')
            entry.delete(0, 'end')
