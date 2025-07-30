import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap import Style
import sqlite3
import pywhatkit
from scripts.database import DataBase

#Intento de MEJORAR LA LOGICA DEL programa
class VentasPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #Base de datos
        self.db = DataBase("database.db")
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

        #Total
        ttk.Label(right_frame, text="Total", font=("Arial", 28, "bold"), foreground="#333", width=12).pack(anchor="nw", pady=2)
       
        self.total_label = ttk.Label(right_frame, text="$ 0.00", font=("Arial", 28, "bold"), foreground="#BFBFBF",  width=12)
        self.total_label.pack(anchor="nw", pady=2)
        
        #Input y labels para el cambio
        ttk.Label(right_frame, text="Efectivo", font=("Arial", 14), foreground="#333", width=12).pack(anchor="nw", pady=(10,2))
        # Variable asociada al Entry
        self.efectivo_var = tk.StringVar()
        self.efectivoEntry = ttk.Entry(right_frame, font=("Arial", 14), width=15, textvariable=self.efectivo_var)
        self.efectivoEntry.pack(pady=(5,5), anchor="w")

        self.change_label = ttkb.Label(right_frame, text="Cambio: $ 0.00", font=("Arial", 14), foreground="#BFBFBF")
        self.change_label.pack(anchor="w", pady=2, fill="x")
        # Detectar cambios en el Entry
        self.efectivo_var.trace_add("write", self.actualizar_cambio)
        

        # --- Checkbox para agregar número de teléfono ---
        self.add_phone_var = tk.BooleanVar(value=False)
        self.print_ticket_var = tk.BooleanVar(value=True)

        self.phone_check = ttk.Checkbutton(
            right_frame,
            text="Enviar compra por WhatsApp",
            variable=self.add_phone_var,
            command=self.toggle_phone_entry
        )
        self.phone_check.pack(anchor="w", pady=(10, 2))

        self.phone_entry = ttk.Entry(right_frame, font=("Arial", 14), width=15)
        self.phone_entry.bind("<KeyRelease>", self.format_phone)

        

        # --- Checkbox para imprimir ticket ---
        self.print_ticket_check = ttk.Checkbutton(
            right_frame,
            text="Imprimir ticket",
            variable=self.print_ticket_var
        )
        self.print_ticket_check.pack(anchor="w", pady=(5, 10))

        # --- Botón de pagar ---
        style = Style()
        style.configure("Custom.TButton", font=("Helvetica", 14))
        self.pay_button = ttk.Button(
            right_frame,
            text="PAGAR",
            bootstyle="danger",
            #style="Custom.TButton",
            command=self.procesar_pago
        )
        self.pay_button.pack(anchor="s", side="bottom",fill="x", pady=(10, 10))

        # Datos internos
        #Productos ahora es un diccionario que contiene el nombre del producto y la cantidad de existencia
        #Puesto que ahora checaremos los cambios a traves de la tabla
        self.productos = {}

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
            self.productos[producto["producto"]] = producto["existencia"]
            if producto["existencia"] > 0:
                result = self.is_product_on_table(producto["producto"])
                if result:
                    cantidad_actual, row_id = result
                    if cantidad_actual+1 <= producto["existencia"]:
                        self.tree.set(row_id, "cantidad", (cantidad_actual + 1))
                        self.barcode_entry.delete(0, tk.END)
                        self.actualizar_total()
                        self.result_label.config(text=f"El producto {producto["producto"]} se agrego exitosamente", bootstyle="success")
                    else:
                        self.result_label.config(text=f"No hay unidades suficientes para vender existencias: {producto["existencia"]}", bootstyle="danger")
                        self.barcode_entry.delete(0, tk.END)
                else:
                    producto["cantidad"] = 1
                    self.insertar_en_tabla(producto)
                    self.barcode_entry.delete(0, tk.END)
                    self.actualizar_total()
                    self.result_label.config(text=f"El producto {producto["producto"]} se agrego exitosamente", bootstyle="success")
                self.actualizar_cambio()
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
            existencia = self.productos[nombre]
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
                self.actualizar_cambio()
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
                
            product_name = self.tree.item(row)['values'][0]
            del self.productos[product_name]
            #Eliminar tambien de la lista
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
    
    def toggle_phone_entry(self):
        if self.add_phone_var.get():
            self.print_ticket_check.pack_forget()
            self.pay_button.pack_forget()
            self.phone_entry.pack(anchor="w", pady=(3, 10))
            self.print_ticket_check.pack(anchor="w", pady=(5, 10))
            self.pay_button.pack(anchor="s",side="bottom",fill="x", pady=(10, 10))
        else:
            self.phone_entry.pack_forget()

    def procesar_pago(self):
        if len(self.productos) > 0:
            try:
                if float(self.efectivoEntry.get()) > 0 and float(self.efectivoEntry.get()) >= float(self.total_label.cget("text")[1:]):
                    if self.add_phone_var.get():
                        print("MANDA WAHTS")
                    if self.print_ticket_var.get():
                        self.send_info_whatsAPP()
                    #Obtener info de los productos
                    products = []
                    cant = 0
                    for row_id in self.tree.get_children():
                        aux = {}
                        p= self.tree.item(row_id)["values"]
                        aux["product_name"] = p[0]
                        aux["price"] = float(p[2][1:])
                        aux["amount"] = int(p[1])
                        cant += aux["amount"]
                        aux["active"] = 1
                        products.append(aux)
                        print(aux)
                    #Incertar en tablas
                    id_sale = self.db.insert("sales", {
                        "total_price": float(self.total_label.cget("text")[2:]),
                        "cash": float(self.efectivoEntry.get()),
                        "change": float(self.change_label.cget("text")[10:]),
                        "total_products": cant,
                        "user": "admin",
                        "active": 1
                        # "date" no es necesario, se agrega automáticamente
                    })
                    #Descontar los productos y registrarlos en la tabla de enta
                    for p in products:
                        p["id_sale"] = id_sale
                        self.db.insert("salesDetail", p)
                        self.db.modify("inventory", 
                                       {"product_name": p["product_name"]}, 
                                       {"amount": self.productos[p["product_name"]] - p["amount"]})
                    #Limpiar todo 
                    self.clean_sale()
                    self.result_label.config(text="Se realizo la venta", bootstyle="success")
                    return
                else:
                    self.result_label.config(text="Ingresa efectivo suficiente para relizar la venta", bootstyle="danger")
            except ValueError:
                self.result_label.config(text=ValueError)
                return
        else:
            self.result_label.config(text="Agrega productos antes de realizar una venta", bootstyle="danger")
            return
        # Aquí iría la lógica de cobro, validaciones, ticket, etc.
    
    def send_info_whatsAPP(self):
        number = "+52" + self.phone_entry.get().strip()
        message = "✏️Pepeleria el Guerrero Dragon\n" \
                    "Detalle de compra:\n"
        
        for row_id in self.tree.get_children():
            p= self.tree.item(row_id)["values"]
            aux = f"  • {p[1]} {p[0]}: ${(float(p[1]) * float(p[2][1:])):.2f}\n "
            message += aux
        message += f"Total:    {self.total_label.cget("text")} \n"
        message += f"Efectivo: ${self.efectivoEntry.get()} \n"
        message += f"Cambio:   ${self.change_label.cget("text")[10:]}\n"
        message += "Gracias por tu preferencia (:"
        print(message)
        #try:
        #    pywhatkit.sendwhatmsg_instantly(number, message)
        #    print("Mensaje enviado (o se intentó enviar).")
        #except Exception as e:
        #    print(f"Ocurrió un error: {e}")

    def actualizar_cambio(self, *args):
        try:
            if len(self.efectivo_var.get()) > 0:
                efectivo = float(self.efectivo_var.get())
                cambio = efectivo - float(self.total_label.cget("text")[1:])
                if cambio < 0:
                    self.change_label.config(text="Cambio: $ 0.00", foreground="#CA5555")
                else:
                    self.change_label.config(text=f"Cambio: $ {cambio:.2f}", foreground="#5ABB7A")
            else:
                self.change_label.config(text="Cambio: $ 0.00", foreground="#BFBFBF")
        except ValueError:
            self.change_label.config(text="Cambio: $ 0.00", foreground="#DDB547")

    def format_phone(self, event=None):
        # Get the original cursor position
        original_cursor = self.phone_entry.index(tk.INSERT)

        # Get raw digits
        raw = ''.join(filter(str.isdigit, self.phone_entry.get()))
        raw = raw[:10]

        # Format the string
        formatted = ""
        for i, digit in enumerate(raw):
            if i == 3 or i == 6:
                formatted += " "
                if original_cursor > i:
                    original_cursor += 1  # adjust cursor for added space
            formatted += digit

        # Update entry and cursor
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, formatted)
        self.phone_entry.icursor(min(original_cursor, len(formatted)))
    
    def clean_sale(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.productos = {}
        self.phone_entry.delete(0, tk.END)
        self.efectivoEntry.delete(0, tk.END)
        self.actualizar_total()
        self.actualizar_cambio()