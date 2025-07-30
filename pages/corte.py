import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import ttkbootstrap as ttkb
from scripts.database import DataBase

class CortePage(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.db = DataBase("database.db")
        self.user = user

        # Título
        ttkb.Label(self, text="💰 Corte de caja", font=("Helvetica", 20, "bold"), bootstyle="primary").pack(anchor='nw', padx=30, pady=(20, 5))

        # Fila de información y botón
        info_frame = ttkb.Frame(self)
        info_frame.pack(fill='x', padx=30, pady=(5, 10))

        self.total_label = ttkb.Label(info_frame, text="Total: $0.00", font=("Helvetica", 14))
        self.total_label.pack(side='left')

        if self.user["type"] == 0:
            historial_button = ttkb.Button(info_frame, text="Historial de cortes", bootstyle="info-outline")
            historial_button.pack(side='right')

        # Filtros
        filter_frame = ttkb.Frame(self)
        filter_frame.pack(fill='x', padx=30, pady=(0, 10))
        ttkb.Label(filter_frame, text="Ordenar por:", font=("Helvetica", 12, "bold")).pack(side='left', padx=(0,10))

        self.filtro_var = tk.StringVar(value="2")

        ttkb.Radiobutton(filter_frame, text="Precio ↑", variable=self.filtro_var, value="0", bootstyle="secondary").pack(side='left', padx=10)
        ttkb.Radiobutton(filter_frame, text="Precio ↓", variable=self.filtro_var, value="1", bootstyle="secondary").pack(side='left', padx=10)
        ttkb.Radiobutton(filter_frame, text="Fecha ↑", variable=self.filtro_var, value="2", bootstyle="secondary").pack(side='left', padx=10)
        ttkb.Radiobutton(filter_frame, text="Fecha ↓", variable=self.filtro_var, value="3", bootstyle="secondary").pack(side='left', padx=10)

        # Tabla
        table_frame = ttkb.Frame(self)
        table_frame.pack(fill='both', expand=True, padx=30, pady=(0, 10))

        self.scrollbar = ttkb.Scrollbar(table_frame)
        self.scrollbar.pack(side='right', fill='y')

        self.tree = ttk.Treeview(table_frame, columns=("id", "fecha", "total", "usuario"),
                                 show="headings", yscrollcommand=self.scrollbar.set, height=12)

        self.tree.heading("id", text="ID")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("total", text="Total")
        self.tree.heading("usuario", text="Usuario")

        self.tree.column("id", width=50, anchor='center')
        self.tree.column("fecha", width=150, anchor='center')
        self.tree.column("total", width=100, anchor='center')
        self.tree.column("usuario", width=150, anchor='center')

        self.tree.pack(side='left', fill='both', expand=True)
        self.scrollbar.config(command=self.tree.yview)

        # Botón Corte
        corte_button = ttkb.Button(self, text="Corte", bootstyle="danger", width=20)
        corte_button.pack(pady=(5, 20))
