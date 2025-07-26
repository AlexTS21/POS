import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import sqlite3
from ttkbootstrap import Style
import pages.registrarProducto as RP
import pages.modificarProducto as MP
from tkinter import Tk, StringVar

class InventarioPage(ttkb.Frame):
    def __init__(self, parent):
        super().__init__(parent )#, padding=20)
        self.Frame = ttkb.Frame 
        ttkb.Label(self, text="📦 Inventario", font=("Helvetica", 20, "bold"), bootstyle="primary").pack(anchor='nw', padx=30, pady=10)
        #Mantener id de productos
        self.products = []


        style = Style()
        style.configure("Custom.TButton", font=("Helvetica", 14))
        # Input and button
        input_frame = ttkb.Frame(self)
        input_frame.pack(pady=5, fill='x', padx=(30, 30))  # Make it stretch horizontally

        # Label and Entry aligned left
        ttkb.Label(input_frame, text="Escanea el código o escríbelo:", font=("Helvetica", 12))\
            .grid(column=0, row=0, columnspan=2, sticky='w', pady=(10, 5))

        self.entry = ttkb.Entry(input_frame, font=("Helvetica", 14), width=30)
        self.entry.grid(column=0, row=1, padx=(0, 10), sticky='w')

        # Spacer column to push the button to the right
        input_frame.grid_columnconfigure(1, weight=1)

        # Button aligned right
        ttkb.Button(
            input_frame,
            text="REGISTRAR PRODUCTOS",
            bootstyle="success",
            command=self.show_register_form,
            style="Custom.TButton"
        ).grid(column=2, row=1, sticky='e')


        self.result_label = ttkb.Label(input_frame, text="", font=("Helvetica", 12), bootstyle="info")
        self.result_label.grid(column=0, row=2, columnspan=3, pady=(5, 5), sticky='w')
        # Filtros
        filter_frame = ttkb.Frame(self)
        filter_frame.pack( fill='x', padx=(30, 30), pady=(0,10))  # Estira horizontalmente

        # ========== FILA 1: Filtro de Ordenamiento ==========
        ttkb.Label(filter_frame, text="Ordenar por:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w", padx=(0,5))

        self.var_sort = ttkb.StringVar(value="0")

        ttkb.Radiobutton(filter_frame, text="Precio ↑", variable=self.var_sort, value="0", bootstyle="info", command=lambda: self.aplicar_filtros(self.products)).grid(row=0, column=1, padx=5)
        ttkb.Radiobutton(filter_frame, text="Precio ↓", variable=self.var_sort, value="1", bootstyle="info", command=lambda: self.aplicar_filtros(self.products)).grid(row=0, column=2, padx=5)
        ttkb.Radiobutton(filter_frame, text="Cantidad ↑", variable=self.var_sort, value="2", bootstyle="info", command=lambda: self.aplicar_filtros(self.products)).grid(row=0, column=3, padx=5)
        ttkb.Radiobutton(filter_frame, text="Cantidad ↓", variable=self.var_sort, value="3", bootstyle="info", command=lambda: self.aplicar_filtros(self.products)).grid(row=0, column=4, padx=5)

        # ========== FILA 2: Filtro por Tipo de Unidad ==========
        ttkb.Label(filter_frame, text="Tipo de unidad:", font=("Helvetica", 12, "bold")).grid(row=0, column=5, sticky="w", padx=5)

        self.tipo_var = ttkb.StringVar(value="3")  # Todos por defecto

        ttkb.Radiobutton(filter_frame, text="Todos", variable=self.tipo_var, value="3", bootstyle="info", command=lambda: self.aplicar_filtros(self.products)).grid(row=0, column=6, padx=5)
        ttkb.Radiobutton(filter_frame, text="Pieza", variable=self.tipo_var, value="0", bootstyle="info", command=lambda: self.aplicar_filtros(self.products)).grid(row=0, column=7, padx=5)
        ttkb.Radiobutton(filter_frame, text="Caja", variable=self.tipo_var, value="1", bootstyle="info", command=lambda: self.aplicar_filtros(self.products)).grid(row=0, column=8, padx=5 )
        ttkb.Radiobutton(filter_frame, text="Metro", variable=self.tipo_var, value="2", bootstyle="info", command=lambda: self.aplicar_filtros(self.products)).grid(row=0, column=9, padx=5)



        # Table and scrollbar
        table_frame = ttkb.Frame(self)
        table_frame.pack(fill='both', expand=True, pady=10, padx=(30, 30))

        scrollbar = ttkb.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')

        # Add treeview
        self.tree = ttkb.Treeview(
            table_frame,
            columns=('ID', 'Código', 'Producto', 'Precio', 'Cantidad', 'Unidad', 'Herramientas'),
            show='headings',
            yscrollcommand=scrollbar.set,
            height=10
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Código', text='Código')
        self.tree.heading('Producto', text='Producto')
        self.tree.heading('Precio', text='Precio')
        self.tree.heading('Cantidad', text='Cantidad')
        self.tree.heading('Unidad', text='Unidad')
        self.tree.heading('Herramientas', text='Herramientas')

        self.tree.column('ID', width=30, anchor='center')
        self.tree.column('Código', width=100,anchor='center')
        self.tree.column('Producto', width=150, anchor='center')
        self.tree.column('Precio', width=80, anchor='center')
        self.tree.column('Cantidad', width=80, anchor='center')
        self.tree.column('Unidad', width=80, anchor='center')
        self.tree.column('Herramientas', width=100, anchor='center')

        self.tree.pack(fill='both', expand=True)

        self.tree.bind("<Button-1>", self.on_tree_click)

        self.load_active_products()
        self.entry.bind("<Return>", self.process_input)

    def process_input(self, event=None):
        code = self.entry.get().strip()
        if code:
            self.search_product(code)
            if len(self.products) > 0:
                self.aplicar_filtros(self.products)
                self.result_label.config(text=f"Código ingresado: {code}", bootstyle="success")
            else:
                self.result_label.config(text=f"Producto no encontrado", bootstyle="danger")
            self.entry.delete(0, 'end')



    def aplicar_filtros(self, ids):
       
        sort_val = self.var_sort.get()
        tipo_val = self.tipo_var.get()

        if not ids:
            self.display_products([])
            return

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Base query
        query = f"""
            SELECT id, barcode, product_name, price, amount, unit_type 
            FROM inventory 
            WHERE active = 1 AND id IN ({','.join('?' * len(ids))})
        """
        params = ids.copy()

        # Filtro por tipo de unidad
        if tipo_val != "3":  # Si no es "Todos"
            query += " AND unit_type = ?"
            params.append(int(tipo_val))

        # Ordenamiento
        sort_columns = {
            "0": "price ASC",
            "1": "price DESC",
            "2": "amount ASC",
            "3": "amount DESC"
        }
        query += f" ORDER BY {sort_columns.get(sort_val, 'id DESC')}"

        cursor.execute(query, params)
        products = cursor.fetchall()
        conn.close()

        # Convertir a lista de dicts para mostrar
        product_dicts = []
        for row in products:
            product_dicts.append({
                'id': row[0],
                'barcode': row[1],
                'product_name': row[2],
                'price': row[3],
                'amount': row[4],
                'unit_type': row[5]
            })

        self.display_products(product_dicts)

    
    def search_product(self, code):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Buscar coincidencias parciales en barcode o product_name
        query = """
            SELECT id
            FROM inventory 
            WHERE active = 1 AND (barcode LIKE ? OR product_name LIKE ?)
        """

        wildcard_code = f"%{code}%"
        cursor.execute(query, (wildcard_code, wildcard_code))
        rows = cursor.fetchall()
        conn.close()

        # Empaquetar como lista de diccionarios
        products = []
        for row in rows:
            products.append(row[0])
        self.products = products
        

    def display_products(self, products):
        # Limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        products.reverse()
        for product in products:
            unidad_str = self.unit_type_to_text(product['unit_type'])
            self.tree.insert(
                '', 'end',
                values=(
                    product['id'],
                    product['barcode'],
                    product['product_name'],
                    f"${product['price']:.2f}",
                    product['amount'],
                    unidad_str,
                    "Modificar"
                )
            )

    def unit_type_to_text(self, unit_type):
        return {
            0: "Pieza",
            1: "Caja",
            2: "Metro"
        }.get(unit_type, "Desconocido")



    def load_active_products(self):
        """Load active products from SQLite into the table."""
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert products
        cursor.execute("SELECT id, barcode, product_name, price, amount, unit_type FROM inventory WHERE active = 1")
        products = cursor.fetchall()
        products.reverse()
        for row in products:
            id_, barcode, name, price, amount, unit_type = row
            unidad_str = self.unit_type_to_text(unit_type)
            self.tree.insert('', 'end', values=(id_, barcode, name, f"${price:.2f}", amount, unidad_str, "Modificar"))
            self.products.append(id_)
        conn.close()

    def on_tree_click(self, event):
        """Handle click on 'Modificar' cell."""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            row_id = self.tree.identify_row(event.y)
            col_index = int(column.replace("#", "")) - 1

            if col_index == 6:  # Herramientas column index
                item = self.tree.item(row_id)
                product_data = item['values']
                self.modify_product(product_data)

    def modify_product(self, product_data):
        """Modify product handler"""
        product_id = product_data[0]
        print(f"Modificar producto ID {product_id} - TODO: abrir ventana de edición")
        self.show_modify_form(product_id)
        # You can implement a pop-up window to edit this product's data

    def show_register_form(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()
        RP.RegistroProductoPage(self.master, self.return_to_inventory).pack(fill='both', expand=True)

    def return_to_inventory(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()
        self.pack(fill='both', expand=True)
        self.load_active_products()

    def show_modify_form(self, id):
        for widget in self.master.winfo_children():
            widget.pack_forget()
        MP.ModificarProductoPage(self.master, self.return_to_inventory, id).pack(fill='both', expand=True)


