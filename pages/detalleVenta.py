import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import ttk
from ttkbootstrap import Style
from scripts.database import DataBase

#0 pieza 1 caja 2 metro
class DetalleVentaPage(ttkb.Frame):
    def __init__(self, parent, go_back_callback, id, backTo):
        super().__init__(parent)
        self.db = DataBase("database.db")
        ttkb.Label(self, text="🏷️Detalle de la venta", font=("Helvetica", 20, "bold"), bootstyle="primary").pack(anchor='nw', padx=30, pady=10)
 
        info_frame = ttkb.Frame(self)
        info_frame.pack(padx=50, pady=10, fill='x')
        info_frame.grid_columnconfigure(3, weight=1)
        ttkb.Button(info_frame, text=backTo, bootstyle="secondary",  command=go_back_callback).grid(row=0, column=3, sticky='e', pady=5)
        ttkb.Label(info_frame, text="Información:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w", padx=(0,5))
        
        #Obtener la venta con id
        venta = self.db.search("sales", {"id":id}, ["total_price", "cash", "change", "total_products", "user", "date"] )[0]
        
        names_venta={
            "total_price": "Total",
            "cash": "Efectivo",
            "change": "Cambio",
            "total_products": "Total de productos",
            "user": "Usuario",
            "date": "Fecha"
        }
        ttkb.Label(info_frame, text=f'id:').grid(row=1, column=1, sticky="w", padx=(45,5))
        ttkb.Label(info_frame, text=id).grid(row=1, column=2, sticky="w", padx=(0,5))
        for i, item in enumerate(venta.items()):
            key, atrib = item
            ttkb.Label(info_frame, text=f'{names_venta[key]}:').grid(row=i+2, column=1, sticky="w", padx=(45,5))
            if i<3:
                ttkb.Label(info_frame, text=f'${atrib}').grid(row=i+2, column=2, sticky="w", padx=(0,5))
            else:
                ttkb.Label(info_frame, text=f'{atrib}').grid(row=i+2, column=2, sticky="w", padx=(0,5))

        table_frame = ttkb.Frame(self)
        table_frame.pack(fill='both', expand=True, padx=30, pady=(0, 10))

        self.scrollbar = ttkb.Scrollbar(table_frame)
        self.scrollbar.pack(side='right', fill='y')

        self.tree = ttk.Treeview(table_frame, columns=("producto", "precio", "cantidad", "total"),
                                 show="headings", yscrollcommand=self.scrollbar.set, height=12)

        self.tree.heading("producto", text="Producto")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("total", text="Total")

        self.tree.column("producto", width=100, anchor='center')
        self.tree.column("precio", width=100, anchor='center')
        self.tree.column("cantidad", width=100, anchor='center')
        self.tree.column("total", width=100, anchor='center')

        self.tree.pack(side='left', fill='both', expand=True)
        self.scrollbar.config(command=self.tree.yview)

        #Cargar los productos a la tabla
        sales = self.db.get_detalles_venta(id)
        for sale in sales:
            self.tree.insert(
                '', 'end',
                values=(
                    sale['product_name'],
                    f"${sale['price']}",
                    sale['amount'],
                    f"${(float(sale['price'])*float(sale['amount'])):.2f}",
                )
            )