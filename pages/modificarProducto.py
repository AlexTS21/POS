import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import sqlite3
from ttkbootstrap import Style
import random
#0 pieza 1 caja 2 metro
class ModificarProductoPage(ttkb.Frame):
    def __init__(self, parent, go_back_callback, id):
        super().__init__(parent)
        self.product = self.get_product_info(id)
        ttkb.Label(self, text="✏️Modificar producto", font=("Helvetica", 20, "bold"), bootstyle="primary").pack(anchor='nw', padx=30, pady=10)

        info_frame = ttkb.Frame(self)
        info_frame.pack(padx=50, pady=10, fill='x')
        ttkb.Button(info_frame, text="Volver al inventario", bootstyle="secondary",  command=go_back_callback).grid(row=0, column=2, sticky='w', pady=5)

        ttkb.Label(info_frame, text="Información:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w", padx=(0,5))
        #Informacion de los productos
        ttkb.Label(info_frame, text=f'Id:       {id}', font=("Helvetica", 12)).grid(row=1, column=1, sticky="w", padx=(0,5))
        ttkb.Label(info_frame, text=f'Codigo:   {self.product['code']}', font=("Helvetica", 12)).grid(row=2, column=1, sticky="w", padx=(0,5))
        ttkb.Label(info_frame, text=f'Producto: {self.product['product_name']}', font=("Helvetica", 12)).grid(row=3, column=1, sticky="w", padx=(0,5))
        ttkb.Label(info_frame, text=f'Precio:      {str(self.product['price'])}', font=("Helvetica", 12)).grid(row=4, column=1, sticky="w", padx=(0,5))
        ttkb.Label(info_frame, text=f'Cantidad: {self.product['amount']}', font=("Helvetica", 12)).grid(row=5, column=1, sticky="w", padx=(0,5))

        #OBtener la informacion de los productos

        form_frame = ttkb.Frame(self)
        form_frame.pack(padx=50, pady=10, fill='x')

        #Agregar el campo de Modificar Precio y Cantidad a aumentar
        self.entries = {}
        self.generate_var = ttkb.IntVar()
        ttkb.Label(form_frame, text="Precio:", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.precio = ttkb.Entry(form_frame,  font=("Helvetica", 12))
        self.precio.grid(row=0, column=1, sticky="ew", pady=5)

        ttkb.Label(form_frame, text="Cantidad a aumentar:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.cantidad = ttkb.Entry(form_frame,  font=("Helvetica", 12))
        self.cantidad.grid(row=1, column=1, sticky="ew", pady=5)
       

        form_frame.grid_columnconfigure(1, weight=1)

       
        self.infoLabel = ttkb.Label(form_frame, text="", font=("Helvetica", 12), bootstyle="info")
        self.infoLabel.grid(row=2, column=1, sticky="w", pady=5)

        button_frame = ttkb.Frame(self)
        button_frame.pack(pady=15)

        ttkb.Button(button_frame, text="Eliminar producto", bootstyle="danger", command=lambda: self.eliminar_producto(id)).pack(side="left", padx=10)
        ttkb.Button(button_frame, text="Guardar Cambios", bootstyle="success", command=self.registrar_Producto).pack(side="left", padx=10)

    def get_product_info(self, id):
        #Coneccion a la base de datos
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT barcode, product_name, price, amount, unit_type FROM inventory WHERE  id=?", (id,))
        product = cursor.fetchone()
        
        if product:
            conn.commit()
            conn.close()
            return  {
                "id": id,
                "code": product[0],
                "product_name": product[1],
                "price": product[2],
                "amount": product[3],
                "unit_type": product[4]
            }
        conn.commit()
        conn.close()
        return None
    
    def eliminar_producto(self, id_producto):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE inventory SET active = 0 WHERE id = ?", (id_producto,))
            conn.commit()
            conn.close()
            self.infoLabel.config(text=f'El producto con ID {id_producto} fue eliminado',bootstyle="success")
            print(f"Producto con ID {id_producto} desactivado correctamente.")
        except sqlite3.Error as e:
            self.infoLabel.config(text=f'Error: {e}',bootstyle="danger")

            print(f"Error al desactivar el producto: {e}")
            

    def registrar_Producto(self):
        #if self.check_entery():
            codigo = self.entries['código'].get()
            nombre = self.entries['nombre del producto'].get()
            precio = float(self.entries['precio'].get())
            cantidad = int(self.entries['cantidad'].get())
            #Coneccion a la base de datos
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
            INSERT OR IGNORE INTO inventory (barcode, product_name, price, amount, unit_type, active)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (codigo, nombre, precio, cantidad, int(self.tipo_var.get()), 1))

            # Commit changes and close connection
            conn.commit()
            conn.close()
            self.infoLabel.config(text=f"Proucto {nombre} registrado", bootstyle="success")
            print("Base de datos registro")
    
    