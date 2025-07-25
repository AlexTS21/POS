import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import sqlite3
from ttkbootstrap import Style
import random

class RegistroProductoPage(ttkb.Frame):
    def __init__(self, parent, go_back_callback):
        super().__init__(parent)

        ttkb.Label(self, text="➕ Registrar nuevo producto", font=("Helvetica", 20, "bold"), bootstyle="primary").pack(anchor='nw', padx=30, pady=10)

        form_frame = ttkb.Frame(self)
        form_frame.pack(padx=50, pady=10, fill='x')

        style = Style()
        style.configure("Custom.TButton", font=("Helvetica", 14))

        labels = ["Código", "Nombre del producto", "Precio", "Cantidad"]
        self.entries = {}
        self.generate_var = ttkb.IntVar()

        ttkb.Button(form_frame, text="Volver al inventario", bootstyle="secondary",  command=go_back_callback).grid(row=0, column=2, sticky='e', pady=5)

        for i, label in enumerate(labels):
            ttkb.Label(form_frame, text=label + ":", font=("Helvetica", 12)).grid(row=i+1, column=0, sticky="w", pady=5)

            entry = ttkb.Entry(form_frame,  font=("Helvetica", 12))
            entry.grid(row=i+1, column=1, sticky="ew", pady=5)
            self.entries[label.lower()] = entry

            # Si es el campo Código, agregamos el checkbox "Generar"
            if label == "Código":
                generar_checkbox = ttkb.Checkbutton(
                    form_frame,
                    text="Generar",
                    variable=self.generate_var,
                    command=self.toggle_codigo_entry,
                    bootstyle="info"
                )
                generar_checkbox.grid(row=i+1, column=2, padx=10)

        form_frame.grid_columnconfigure(1, weight=1)
        self.infoLabel = ttkb.Label(form_frame, text="", font=("Helvetica", 12), bootstyle="info")
        self.infoLabel.grid(row=5, column=1, sticky="w", pady=5)
        button_frame = ttkb.Frame(self)
        button_frame.pack(pady=15)

        ttkb.Button(button_frame, text="Registrar producto", bootstyle="success", command=self.registrar_Producto).pack(side="left", padx=10)
    
    def registrar_Producto(self):
        if self.check_entery():
            codigo = self.entries['código'].get()
            nombre = self.entries['nombre del producto'].get()
            precio = float(self.entries['precio'].get())
            cantidad = int(self.entries['cantidad'].get())
            #Coneccion a la base de datos
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
            INSERT OR IGNORE INTO inventory (barcode, product_name, price, amount, active)
            VALUES (?, ?, ?, ?, ?)
            ''', (codigo, nombre, precio, cantidad, 1))

            # Commit changes and close connection
            conn.commit()
            conn.close()
            self.infoLabel.config(text=f"Proucto {nombre} registrado", bootstyle="success")
            print("Base de datos registro")
    
    def check_entery(self):
        for entry in self.entries.values():
            if len(str(entry.get())) == 0:
                #Show message
                self.infoLabel.config(text="Rellena todos los campos por favor", bootstyle="warning")
                return None
        #Codigo
        try:
            int(self.entries["código"].get())
            if len(self.entries["código"].get()) < 10:
                self.infoLabel.config(text="El codigo de barras tiene que tener mas de 10 digitos", bootstyle="warning")
                return None
            codigos = self.obtener_codigos()
            if self.entries["código"].get() in codigos:
                self.infoLabel.config(text="El codigo de barras ya existe en la base", bootstyle="warning")
                return None
        except ValueError:
            self.infoLabel.config(text="El codigo tiene que ser un numero entero", bootstyle="warning")
            return None
        
        #precio
        try:
            if float(self.entries["precio"].get()) < 0:
                self.infoLabel.config(text="Introdusca un precio positivo", bootstyle="warning")
                return None
        except ValueError:
            self.infoLabel.config(text="El precio tiene que ser un numero", bootstyle="warning")
            return None
        #cantidad
        try:
            if int(self.entries["cantidad"].get()) < 0:
                self.infoLabel.config(text="Introdusca una cantidad positiva", bootstyle="warning")
                return None
        except ValueError:
            self.infoLabel.config(text="La cantidad tiene que ser un numero entero", bootstyle="warning")
            return None
        return 1

    def obtener_codigos(self):
        # Conexión a la base de datos
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT barcode
            FROM inventory 
        ''')

        # Obtener todos los resultados como lista de tuplas
        resultados = cursor.fetchall()

        # Extraer solo los códigos de las tuplas
        codigos = [fila[0] for fila in resultados]

        conn.close()
        return codigos


    def toggle_codigo_entry(self):
        entry = self.entries["código"]
        codigos = self.obtener_codigos()
        if self.generate_var.get() == 1:
            random_code = ''.join(str(random.randint(0, 9)) for _ in range(12))
            while random_code in codigos:
                random_code = ''.join(str(random.randint(0, 9)) for _ in range(12))
            entry.delete(0, 'end')
            entry.insert(0, random_code)
            entry.config(state='disabled')
        else:
            entry.config(state='normal')


    
        