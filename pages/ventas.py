import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import ttkbootstrap as ttkb
import sqlite3

class VentasPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttkb.Label(self, text="🛒 Ventas", font=("Helvetica", 20, "bold"), bootstyle="primary").pack(anchor='nw', padx=30, pady=10)

        # Layout principal dividido en dos columnas
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- LADO IZQUIERDO: Entrada + Tabla ---
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True)

         # Label and Entry aligned left
        ttkb.Label(left_frame, text="Escanea el código o escríbelo:", font=("Helvetica", 12))\
            .pack(pady=(10,5), side="top", fill="x")

        self.barcode_entry = ttk.Entry(left_frame, font=("Arial", 14), width=30)
        self.barcode_entry.pack(pady=(5,5), anchor="w")
        self.barcode_entry.bind("<Return>", self.agregar_producto)

        self.result_label = ttkb.Label(left_frame, text="", font=("Helvetica", 12), bootstyle="info")
        self.result_label.pack(pady=(5,10),  anchor="w")

        table_frame = ttk.Frame(left_frame)
        table_frame.pack(fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(table_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(table_frame, columns=("producto", "cantidad", "precio", "unidad", "acciones"),
                                 show="headings", yscrollcommand=self.scrollbar.set, height=12)

        self.tree.heading("producto", text="Producto")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("unidad", text="Unidad")
        self.tree.heading("acciones", text="Acciones")

        self.tree.column("producto", width=70, anchor='center')
        self.tree.column("cantidad", width=30, anchor='center')
        self.tree.column("precio", width=40, anchor='center')
        self.tree.column("unidad", width=40, anchor='center')
        self.tree.column("acciones", width=10, anchor='center')

        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.tree.yview)

        # --- SEPARADOR VERTICAL ---
        separator = ttk.Separator(main_frame, orient='vertical')
        separator.pack(side="left", fill="y", padx=(20,5))

        # --- LADO DERECHO: Total ---
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="left", padx=(2, 4), fill="y")


        ttk.Label(right_frame, text="Total", font=("Arial", 28, "bold"), foreground="#333", width=12).pack(anchor="nw", pady=2)
       
        self.total_label = ttk.Label(right_frame, text="$ 0.00", font=("Arial", 28, "bold"), foreground="#BFBFBF",  width=12)
        self.total_label.pack(anchor="nw", pady=2)
        
        
        
        # Datos internos
        self.productos = []

        # Eventos
        self.tree.bind("<Double-1>", self.editar_cantidad)
        self.tree.bind("<Button-1>", self.borrar_producto)

    def agregar_producto(self, event=None):
        codigo = self.barcode_entry.get().strip()
        if not codigo:
            return

        #Consultar la base de datos
        producto = self.get_Product(codigo)
        if producto:
            if producto["existencia"] > 0:
                result = self.is_product_on_table(producto["producto"])
                if result:
                    cantidad_actual, row_id = result
                    if cantidad_actual+1 <= producto["existencia"]:
                        producto["cantidad"] = cantidad_actual + 1
                        nueva_cantidad = cantidad_actual + 1
                        self.tree.set(row_id, "cantidad", nueva_cantidad)
                        self.barcode_entry.delete(0, tk.END)
                        self.actualizar_total()
                        self.result_label.config(text=f"El producto {producto["producto"]} se agrego exitosamente", bootstyle="success")
                    else:
                        self.result_label.config(text=f"No hay unidades suficientes para vender existencias: {producto["existencia"]}", bootstyle="danger")
                        self.barcode_entry.delete(0, tk.END)
                else:
                    producto["cantidad"] = 1
                    self.productos.append(producto)
                    self.insertar_en_tabla(producto)
                    self.barcode_entry.delete(0, tk.END)
                    self.actualizar_total()
                    self.result_label.config(text=f"El producto {producto["producto"]} se agrego exitosamente", bootstyle="success")

            else:
                self.result_label.config(text=f"El producto {producto["producto"]} no puede ser vendido porque no hay existencias", bootstyle="danger")
                self.barcode_entry.delete(0, tk.END)
        else:
            self.result_label.config(text="Producto no encontrado en el inventario", bootstyle="danger")
            self.barcode_entry.delete(0, tk.END)
    
    def is_product_on_table(self, product_name):
        for row_id in self.tree.get_children():
            item = self.tree.item(row_id)
            codigo_tabla = item["values"][0]  # asumimos que el código está en la columna 0
            if codigo_tabla == product_name:
                cantidad_actual = int(item["values"][1])
                return cantidad_actual, row_id
                break
        return None
    
    def get_product_on_list(self, product_name):
        for p in self.productos:
            if p["producto"] == product_name:
                return p
        return None

    def insertar_en_tabla(self, producto):
        self.tree.insert("", index=0, 
                         values=(producto["producto"], 
                                 producto["cantidad"], 
                                 f"${producto["precio"]}",
                                 producto["unidad"],
                                 "🗑️ Eliminar"))

    def editar_cantidad(self, event):
        region = self.tree.identify_region(event.x, event.y)
        column = self.tree.identify_column(event.x)
        row = self.tree.identify_row(event.y)

        if column == "#2" and region == "cell":  # columna 'cantidad'
            item = self.tree.item(row)
            cantidad_actual = item['values'][1]
            nombre = self.tree.item(row)['values'][0]
            existencia = self.get_product_on_list(nombre)["existencia"]
            # Crear ventana emergente
            top = tk.Toplevel(self)
            top.title("Editar cantidad")
            top.geometry("300x150")
            top.resizable(False, False)
            top.overrideredirect(True)

            # Marco exterior verde (simula el borde)
            borde = ttkb.Frame(top, bootstyle="success", padding=2)
            borde.pack(fill="both", expand=True)

            # Marco interior blanco
            contenido = ttkb.Frame(borde, style="White.TFrame", padding=15)
            contenido.pack(fill="both", expand=True)

            # Estilo blanco para el contenido
            style = ttkb.Style()
            style.configure("White.TFrame", background="white")

            ttkb.Label(contenido, text="Nueva cantidad:", font=("Arial", 12), background="white").pack(pady=(0, 10))

            cantidad_var = tk.IntVar(value=cantidad_actual)
            spinbox = ttkb.Spinbox(contenido, from_=0, to=9999, textvariable=cantidad_var,
                                font=("Arial", 12), width=10)
            spinbox.pack()

        def aceptar():
           
            nueva = cantidad_var.get()
            if nueva >= 0 and nueva <=existencia:
                self.tree.set(row, "cantidad", nueva)
                self.actualizar_total()
                self.result_label.config(text=f"Cantidad actualizada a: {nueva}", bootstyle="success")

            elif nueva > existencia:
                self.result_label.config(text=f"No hay unidades suficientes para vender existencias: {existencia}", bootstyle="danger")

            top.destroy()

        ttkb.Button(contenido, text="Aceptar", bootstyle="success", command=aceptar).pack(pady=(10, 0))

        # Cerrar con ESC
        top.bind("<Escape>", lambda e: top.destroy())

        # Centrar la ventana
        top.update_idletasks()
        x = (top.winfo_screenwidth() - top.winfo_width()) // 2
        y = (top.winfo_screenheight() - top.winfo_height()) // 2
        top.geometry(f"+{x}+{y}")

    def borrar_producto(self, event):
        region = self.tree.identify_region(event.x, event.y)
        column = self.tree.identify_column(event.x)
        row = self.tree.identify_row(event.y)

        if column == "#5" and region == "cell":  # columna 'acciones'
            #Descomentar para ventana de dialogo
            #confirm = messagebox.askyesno("Confirmar", "¿Eliminar este producto?")
            #if confirm:
                #Eliminar tambien de la lista
            product_name = self.tree.item(row)['values'][0]
            for i, p in enumerate(self.productos):
                if p['producto'] == product_name:
                    indx = i
                    break
            self.productos.pop(indx)
            self.tree.delete(row)
            self.actualizar_total()
            self.result_label.config(text=f"El producto fue eliminado: {product_name}", bootstyle="warning")


    def actualizar_total(self):
        total = 0
        for row_id in self.tree.get_children():
            cantidad = float(self.tree.item(row_id)['values'][1])
            precio = float(self.tree.item(row_id)['values'][2][1:])
            total += cantidad*precio
        self.total_label.config(text=f"$ {total:.2f}")

    def get_Product(self, code):
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT id, barcode, product_name, amount, unit_type, price FROM inventory WHERE active=1 AND (barcode=? OR product_name=?)", (code, code))
        product = cur.fetchone()
        conn.close()
        unidad = {
            0: "Pieza",
            1: "Caja",
            2: "Metro"
        }
        if product:
            return {
                "id": product[0],
                "codigo": product[1],
                "producto": product[2],
                "existencia": product[3],
                "unidad" : unidad[int(product[4])],
                "precio": product[5]
            }
        return None
