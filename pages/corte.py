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
        info_frame.pack(fill='x', padx=30, pady=(5, 5))

        self.total_label = ttkb.Label(info_frame, text="Total: $0.00", font=("Helvetica", 14))
        self.total_label.pack(side='left')

        if self.user["type"] == 0:
            historial_button = ttkb.Button(info_frame, text="Historial de cortes", bootstyle="info-outline")
            historial_button.pack(side='right')
        
        self.info_corte = ttkb.Label(self, text="Corte sin realizar ✖", font=("Helvetica", 14),bootstyle="danger")
        self.info_corte.pack(pady=(0,7), padx=30, anchor="e", fill="x")
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
        self.tree.heading("acciones", text="Detalles")

        self.tree.column("id", width=50, anchor='center')
        self.tree.column("fecha", width=150, anchor='center')
        self.tree.column("total", width=100, anchor='center')
        self.tree.column("usuario", width=150, anchor='center')
        self.tree.column("acciones", width=150, anchor='center')

        self.tree.bind("<ButtonRelease-1>", self.on_row_click)

        self.tree.pack(side='left', fill='both', expand=True)
        self.scrollbar.config(command=self.tree.yview)

        # Botón Corte
        self.corte_button = ttkb.Button(self, text="Corte", bootstyle="danger", width=20, command=self.make_corte)
        self.corte_button.pack(pady=(5, 20))
        if self.db.corte_realizado_hoy():
            self.info_corte.config(text="Corte relizado ✔",bootstyle="success")
            self.corte_button.config(state="disabled")
        self.sales = []
        self.get_sales()
        self.load_on_table_sales(self.sales)
        self.actualizar_total()
    
    def get_sales(self):
        self.sales = self.db.get_today_cortes()

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
    
    def actualizar_total(self):
        cant = 0
        for s in self.sales:
            cant += float(s["total_price"])
        self.total_label.config(text=f"Total: ${cant}") 
        return cant
    
    def make_corte(self):
        #Revisar si no hay un corte antes
        if not self.db.corte_realizado_hoy():
            #Agregar el corte a la base de datos
            self.db.insert("corte", {
                "total":self.actualizar_total(),
                "user": self.user["username"],
                "active":1
            })
            #Mensaje de exito
            self.info_corte.config(text="Corte relizado ✔",bootstyle="success")
            #Desactivar un boton
            self.corte_button.config(state="disabled")
        return

    def mostrar_detalles_venta(self, venta_id):
        detalles = self.db.get_detalles_venta(venta_id)

        detalle_win = ttkb.Toplevel(self)
        detalle_win.title(f"Detalles de venta #{venta_id}")
        detalle_win.geometry("400x300")
        detalle_win.configure(bg="white")

        marco = ttkb.Frame(detalle_win, padding=10, bootstyle="success")
        marco.pack(fill="both", expand=True)

        ttkb.Label(marco, text=f"Detalles de la venta #{venta_id}", font=("Helvetica", 14, "bold")).pack(pady=10)

        for item in detalles:
            text = f"{item['product_name']} - ${item['price']} x {item['amount']}"
            ttkb.Label(marco, text=text, font=("Helvetica", 12)).pack(anchor='w', padx=10)
    
    def on_row_click(self, event):
        item_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        
        if column == "#5" and item_id:  # Columna 5 = "Detalles"
            venta_id = self.tree.item(item_id)["values"][0]
            self.mostrar_detalles_venta(venta_id)
