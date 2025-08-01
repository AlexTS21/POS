import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import ttk
from ttkbootstrap import Style
from scripts.database import DataBase
import tkinter as tk
import pages.detalleVenta as SD

#0 pieza 1 caja 2 metro
class DetalleCortePage(ttkb.Frame):
    def __init__(self, parent, go_back_callback, corte, backTo):
        super().__init__(parent)
        self.db = DataBase("database.db")
        ttkb.Label(self, text="📇Detalle del corte", font=("Helvetica", 20, "bold"), bootstyle="primary").pack(anchor='nw', padx=30, pady=10)
        info_frame = ttkb.Frame(self)
        info_frame.pack(padx=50, pady=10, fill='x')
        info_frame.grid_columnconfigure(3, weight=1)
        ttkb.Button(info_frame, text=backTo, bootstyle="secondary",  command=go_back_callback).grid(row=0, column=3, sticky='e', pady=5)
        ttkb.Label(info_frame, text="Información:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w", padx=(0,5))
        
        
        for i, item in enumerate(corte.items()):
            key, atrib = item
            ttkb.Label(info_frame, text=f'{key}:').grid(row=i+2, column=1, sticky="w", padx=(45,5))
            ttkb.Label(info_frame, text=f'{atrib}').grid(row=i+2, column=2, sticky="w", padx=(0,5))

        # Filtros
        filter_frame = ttkb.Frame(self)
        filter_frame.pack(fill='x', padx=30, pady=(0, 10))
        ttkb.Label(filter_frame, text="Ordenar por:", font=("Helvetica", 12, "bold")).pack(side='left', padx=(0,10))

        self.filtro_var = tk.StringVar(value="2")

        ttkb.Radiobutton(filter_frame, text="Precio ↑", variable=self.filtro_var, value="0", bootstyle="secondary",  command= self.aplicar_filtros).pack(side='left', padx=10)
        ttkb.Radiobutton(filter_frame, text="Precio ↓", variable=self.filtro_var, value="1", bootstyle="secondary", command= self.aplicar_filtros).pack(side='left', padx=10)
        ttkb.Radiobutton(filter_frame, text="Fecha ↑", variable=self.filtro_var, value="2", bootstyle="secondary", command= self.aplicar_filtros).pack(side='left', padx=10)
        ttkb.Radiobutton(filter_frame, text="Fecha ↓", variable=self.filtro_var, value="3", bootstyle="secondary", command= self.aplicar_filtros).pack(side='left', padx=10)

        # Tabla
        table_frame = ttkb.Frame(self)
        table_frame.pack(fill='both', expand=True, padx=30, pady=(0, 10))

        self.scrollbar = ttkb.Scrollbar(table_frame)
        self.scrollbar.pack(side='right', fill='y')

        self.tree = ttk.Treeview(table_frame, columns=("id", "fecha", "total", "usuario", "acciones"),
                                 show="headings", yscrollcommand=self.scrollbar.set, height=12)

        self.tree.heading("id", text="ID")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("total", text="Total")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("acciones", text="Acciones")

        self.tree.column("id", width=50, anchor='center')
        self.tree.column("fecha", width=150, anchor='center')
        self.tree.column("total", width=100, anchor='center')
        self.tree.column("usuario", width=150, anchor='center')
        self.tree.column("acciones", width=150, anchor='center')

        self.tree.bind("<ButtonRelease-1>", self.on_row_click)

        self.tree.pack(side='left', fill='both', expand=True)
        self.scrollbar.config(command=self.tree.yview)

        #Load Sales 
        self.sales = self.db.search("sales", {"date": corte["Fecha"][:11]}, ["id", "total_price", "cash", "change", "total_products", "user", "date",], strict=False)
        self.load_on_table_sales(self.sales)

    def load_on_table_sales(self, sales):
        for row in self.tree.get_children():
            self.tree.delete(row)
        sales.reverse()
        for sale in sales:
            self.tree.insert(
                '', 'end',
                values=(
                    sale['id'],
                    sale['date'],
                    f"${sale['total_price']:.2f}",
                    sale['user'],
                    "Detalles"
                )
            )

    def aplicar_filtros(self):
        opcion = self.filtro_var.get()
        if opcion == "0":  # Precio ascendente
            sales = sorted(self.sales, key=lambda x: x["total_price"])
        elif opcion == "1":  # Precio descendente
            sales = sorted(self.sales, key=lambda x: x["total_price"], reverse=True)
        elif opcion == "2":  # Fecha ascendente
            sales = sorted(self.sales, key=lambda x: x["date"])
        elif opcion == "3":  # Fecha descendente
            sales = sorted(self.sales, key=lambda x: x["date"], reverse=True)
        self.load_on_table_sales( sales)
        return

    def on_row_click(self, event):
        item_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        
        if column == "#5" and item_id:  # Columna 5 = "Detalles"
            venta_id = self.tree.item(item_id)["values"][0]
            self.show_saleDetail_form(venta_id)

    def return_to_corte(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()
        self.pack(fill='both', expand=True)
        
        
    def show_saleDetail_form(self, id):
        for widget in self.master.winfo_children():
            widget.pack_forget()
        SD.DetalleVentaPage(self.master, self.return_to_corte, id, "Volver al detlle de corte").pack(fill='both', expand=True)

