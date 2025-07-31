import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import ttk
from ttkbootstrap import Style
from scripts.database import DataBase
import tkinter as tk

#0 pieza 1 caja 2 metro
class HistorialCortePage(ttkb.Frame):
    def __init__(self, parent, go_back_callback, backTo):
        super().__init__(parent)
        self.db = DataBase("database.db")
        ttkb.Label(self, text="🕓Historial de Cortes", font=("Helvetica", 20, "bold"), bootstyle="primary").pack(anchor='nw', padx=30, pady=10)


        # Input and button
        input_frame = ttkb.Frame(self)
        input_frame.pack(pady=5, fill='x', padx=(30, 30))  # Make it stretch horizontally

        # Label and Entry aligned left
        ttkb.Label(input_frame, text="Buscar por fecha (año-mes-dia):", font=("Helvetica", 12))\
            .grid(column=0, row=0, columnspan=2, sticky='w', pady=(10, 5))

        self.entry = ttkb.Entry(input_frame, font=("Helvetica", 14), width=30)
        self.entry.grid(column=0, row=1, padx=(0, 10), sticky='w')
        self.entry.bind("<Return>", self.searchDate)

        # Spacer column to push the button to the right
        input_frame.grid_columnconfigure(1, weight=1)

        # Button aligned right
        ttkb.Button(input_frame, text=backTo, bootstyle="secondary",  command=go_back_callback).grid(column=2, row=1, sticky='e')

        self.result_label = ttkb.Label(input_frame, text="", font=("Helvetica", 12), bootstyle="info")
        self.result_label.grid(column=0, row=2, columnspan=3, pady=(5, 5), sticky='w')

        #Filtros
        filter_frame = ttkb.Frame(self)
        filter_frame.pack(fill='x', padx=30, pady=(0, 10))
        ttkb.Label(filter_frame, text="Ordenar por:", font=("Helvetica", 12, "bold")).pack(side='left', padx=(0,10))

        self.filtro_var = tk.StringVar(value="2")

        ttkb.Radiobutton(filter_frame, text="Precio ↑", variable=self.filtro_var, value="0", bootstyle="secondary",  command= self.aplicar_filtros).pack(side='left', padx=10)
        ttkb.Radiobutton(filter_frame, text="Precio ↓", variable=self.filtro_var, value="1", bootstyle="secondary", command= self.aplicar_filtros).pack(side='left', padx=10)
        ttkb.Radiobutton(filter_frame, text="Fecha ↑", variable=self.filtro_var, value="2", bootstyle="secondary", command= self.aplicar_filtros).pack(side='left', padx=10)
        ttkb.Radiobutton(filter_frame, text="Fecha ↓", variable=self.filtro_var, value="3", bootstyle="secondary", command= self.aplicar_filtros).pack(side='left', padx=10)


        #Tabla
        table_frame = ttkb.Frame(self)
        table_frame.pack(fill='both', expand=True, padx=30, pady=(0, 10))

        self.scrollbar = ttkb.Scrollbar(table_frame)
        self.scrollbar.pack(side='right', fill='y')

        self.tree = ttk.Treeview(table_frame, columns=("id", "fecha", "total", "usuario", "acciones"),
                                 show="headings", yscrollcommand=self.scrollbar.set, height=12)

        self.tree.heading("id", text="id")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("total", text="Total")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("acciones", text="Acciones")
        

        self.tree.column("id", width=100, anchor='center')
        self.tree.column("fecha", width=100, anchor='center')
        self.tree.column("total", width=100, anchor='center')
        self.tree.column("usuario", width=100, anchor='center')
        self.tree.column("acciones", width=100, anchor='center')

        self.tree.pack(side='left', fill='both', expand=True)
        self.scrollbar.config(command=self.tree.yview)
        self.tree.bind("<Button-1>", self.detalleCortePage)
        self.cortes = self.db.get_ultimos_cortes()
        self.load_on_table_cortes(self.cortes)
        self.aplicar_filtros()

    def load_on_table_cortes(self, cortes):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for corte in cortes:
            self.tree.insert(
                '', 'end',
                values=(
                    corte['id'],
                    corte['date'],
                    f"${corte['total']:.2f}",
                    corte['user'],
                    "Detalles"
                )
            )
        

    def aplicar_filtros(self):
        opcion = self.filtro_var.get()
        if opcion == "1":  # Precio ascendente
            cortes = sorted(self.cortes, key=lambda x: x["total"])
        elif opcion == "0":  # Precio descendente
            cortes = sorted(self.cortes, key=lambda x: x["total"], reverse=True)
        elif opcion == "3":  # Fecha ascendente
            cortes = sorted(self.cortes, key=lambda x: x["date"])
        elif opcion == "2":  # Fecha descendente
            cortes = sorted(self.cortes, key=lambda x: x["date"], reverse=True)
        self.load_on_table_cortes(cortes)
        return
    
    def searchDate(self, event=None):
        #Buscan con Like por fecha en el input
        self.cortes = self.db.search("corte", {
                                                "date": self.entry.get()
                                                }, ['id', 'date', 'total', 'user'], strict=False)
        cant =len(self.cortes)
        if cant==0:
            self.result_label.config(text=f"No se obtuvieron resultados con: {self.entry.get()}", bootstyle="danger")
        else:
            self.result_label.config(text=f"{cant} resultados con: {self.entry.get()}", bootstyle="success")
        self.entry.delete(0, 'end')
        self.aplicar_filtros()
    
    def detalleCortePage(self):
        return