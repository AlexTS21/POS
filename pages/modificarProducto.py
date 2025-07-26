import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import sqlite3
from ttkbootstrap import Style
import random
import time
#0 pieza 1 caja 2 metro
class ModificarProductoPage(ttkb.Frame):
    def __init__(self, parent, go_back_callback, id):
        super().__init__(parent)
        self.product = self.get_product_info(id)
        ttkb.Label(self, text="✏️Modificar producto", font=("Helvetica", 20, "bold"), bootstyle="primary").pack(anchor='nw', padx=30, pady=10)

        info_frame = ttkb.Frame(self)
        info_frame.pack(padx=50, pady=10, fill='x')
        info_frame.grid_columnconfigure(3, weight=1)
        ttkb.Button(info_frame, text="Volver al inventario", bootstyle="secondary",  command=go_back_callback).grid(row=0, column=3, sticky='e', pady=5)
        ttkb.Label(info_frame, text="Información:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w", padx=(0,5))
        self.LabelsInfo = []
        for i, item in enumerate(self.product.items()):
            key, atrib = item
            ttkb.Label(info_frame, text=f'{key}:').grid(row=i+1, column=1, sticky="w", padx=(45,5))
            self.LabelsInfo.append(ttkb.Label(info_frame, text=f'{atrib}'))
            self.LabelsInfo[i].grid(row=i+1, column=2, sticky="w", padx=(0,5))
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
        ttkb.Button(button_frame, text="Guardar Cambios", bootstyle="success", command=lambda: self.modificar_Producto(id)).pack(side="left", padx=10)

    def get_product_info(self, id):
        #Coneccion a la base de datos
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT barcode, product_name, price, amount, unit_type FROM inventory WHERE  id=?", (id,))
        product = cursor.fetchone()
        unidad = {
            0: "Pieza",
            1: "Caja",
            2: "Metro"
        }
        if product:
            conn.commit()
            conn.close()
            return  {
                "id": id,
                "Codigo": product[0],
                "Producto": product[1],
                "Precio": f'${product[2]}',
                "Cantidad": product[3],
                "Unidad": unidad[int(product[4])]
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
            
    def check_entry(self):
        if len(self.precio.get().strip()) == 0 and len(self.cantidad.get().strip()) == 0:
            self.infoLabel.config(text=f'Rellna alguno de los campos para modificar el producto',bootstyle="warning")
            return None
        if len(self.precio.get().strip()):
            try:
                if float(self.precio.get().strip()) <= 0 :
                    self.infoLabel.config(text=f'El precio debe ser positivo diferente de 0',bootstyle="warning")
                    return None
            except ValueError:
                self.infoLabel.config(text=f'El precio debe ser un número',bootstyle="warning")
                return None
        if len(self.cantidad.get().strip()):
            try:
                if int(self.cantidad.get().strip()) < 0:
                    self.infoLabel.config(text=f'La cantidad debe ser positiva',bootstyle="warning")
            except ValueError:
                self.infoLabel.config(text=f'La cantidad debe de ser un numero entero',bootstyle="warning")
                return None
            
        return True
    
    def modificar_Producto(self, id):
        if self.check_entry():
            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                if len(self.precio.get().strip()) > 0 and len(self.cantidad.get().strip()) > 0: 
                # Actualizar cantidad sumando delta_cantidad al valor actual
                    cursor.execute("""
                        UPDATE inventory
                        SET price = ?, amount = amount + ?
                        WHERE id = ? AND active = 1
                    """, (float(self.precio.get().strip()), int(self.cantidad.get().strip()), id))
                    self.LabelsInfo[3].config(text=f'${str(float(self.precio.get().strip()))}')
                    self.LabelsInfo[4].config(text=str(int(self.cantidad.get().strip()) + int(self.product['Cantidad'])))
                    self.product['Cantidad'] = int(self.product['Cantidad']) + int(self.cantidad.get().strip())
                elif len(self.precio.get().strip()) == 0 and len(self.cantidad.get().strip()) > 0:
                    cursor.execute("""
                        UPDATE inventory
                        SET amount = amount + ?
                        WHERE id = ? AND active = 1
                    """, (int(self.cantidad.get().strip()), id))
                    self.LabelsInfo[4].config(text=str(int(self.cantidad.get().strip()) + int(self.product['Cantidad'])))
                    self.product['Cantidad'] = int(self.product['Cantidad']) + int(self.cantidad.get().strip())

                elif len(self.precio.get().strip()) > 0 and len(self.cantidad.get().strip()) == 0:
                    cursor.execute("""
                        UPDATE inventory
                        SET price = ?
                        WHERE id = ? AND active = 1
                    """, (float(self.precio.get().strip()), id))
                    self.LabelsInfo[3].config(text=f'${str(float(self.precio.get().strip()))}')
                self.infoLabel.config(text=f'Cambios aplicados al producto con id {id}',bootstyle="success")
                self.clean_inputs()
                conn.commit()
                conn.close()
                return True
            except sqlite3.Error as e:
                print("Error al actualizar:", e)
                return False
    
    def clean_inputs(self):
        self.cantidad.delete(0, 'end')
        self.precio.delete(0, 'end')
        