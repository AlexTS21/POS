import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from scripts.database import DataBase

class UsuariosPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.db = DataBase("database.db")
        ttkb.Label(self, text="👥 Usuarios", font=("Helvetica", 20, "bold"), bootstyle="primary").pack(anchor='nw', padx=30, pady=10)
        form_frame = ttk.Frame(self)
        form_frame.pack(anchor='nw', padx=10)

        #Mantener id de productos
        self.products = []


        
        # Input and button
        input_frame = ttkb.Frame(self)
        input_frame.pack(pady=5, fill='x', padx=(30, 30))  # Make it stretch horizontally

        # Label and Entry aligned left
        ttkb.Label(input_frame, text="Nombre de usuario:", font=("Helvetica", 12))\
            .grid(column=0, row=0, columnspan=2, sticky='w', pady=(10, 5))

        self.entry = ttkb.Entry(input_frame, font=("Helvetica", 14), width=30)
        self.entry.grid(column=0, row=1, padx=(0, 10), sticky='w')

        # Spacer column to push the button to the right
        input_frame.grid_columnconfigure(1, weight=1)

        # Button aligned right
        ttkb.Button(
            input_frame,
            text="REGISTRAR USUARIOS",
            bootstyle="success",
            #command=self.show_register_form,
        ).grid(column=2, row=1, sticky='e')


        self.result_label = ttkb.Label(input_frame, text="", font=("Helvetica", 12), bootstyle="info")
        self.result_label.grid(column=0, row=2, columnspan=3, pady=(5, 5), sticky='w')
        # Filtros
        filter_frame = ttkb.Frame(self)
        filter_frame.pack( fill='x', padx=(30, 30), pady=(0,10))  # Estira horizontalmente

        # ========== FILA 2: Filtro por Tipo de Unidad ==========
        ttkb.Label(filter_frame, text="Tipo de usuario:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5)

        self.tipo_var = ttkb.StringVar(value="0")  # Todos por defecto

        ttkb.Radiobutton(filter_frame, text="Todos", variable=self.tipo_var, value="0", bootstyle="info", command=self.aplicar_filtros).grid(row=0, column=1, padx=5)
        ttkb.Radiobutton(filter_frame, text="Administrador", variable=self.tipo_var, value="1", bootstyle="info", command=self.aplicar_filtros).grid(row=0, column=2, padx=5)
        ttkb.Radiobutton(filter_frame, text="Vendedor", variable=self.tipo_var, value="2", bootstyle="info", command=self.aplicar_filtros).grid(row=0, column=3, padx=5 )



        # Table and scrollbar
        table_frame = ttkb.Frame(self)
        table_frame.pack(fill='both', expand=True, pady=10, padx=(30, 30))

        scrollbar = ttkb.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')

        # Add treeview
        self.tree = ttkb.Treeview(
            table_frame,
            columns=('ID', 'username', 'fullname', 'phone', 'type', 'modificar', 'acciones'),
            show='headings',
            yscrollcommand=scrollbar.set,
            height=10
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.heading('ID', text='id')
        self.tree.heading('username', text='Usuario')
        self.tree.heading('fullname', text='Nombre')
        self.tree.heading('phone', text='Telefono')
        self.tree.heading('type', text='Tipo')
        self.tree.heading('modificar', text='Herramientas')
        self.tree.heading('acciones', text='Acciones')

        self.tree.column('ID', width=30, anchor='center')
        self.tree.column('username', width=100,anchor='center')
        self.tree.column('fullname', width=150, anchor='center')
        self.tree.column('phone', width=80, anchor='center')
        self.tree.column('type', width=80, anchor='center')
        self.tree.column('modificar', width=80, anchor='center')
        self.tree.column('acciones', width=100, anchor='center')

        self.tree.pack(fill='both', expand=True)

        self.tree.bind("<Button-1>", self.on_tree_click)

        self.entry.bind("<Return>", self.process_input)

        self.users = self.db.search("users", {"active":1}, ["id", "username", "fullname", "phone", "type"])
        self.load_users_on_table(self.users)

    def load_users_on_table(self, users):
        for row in self.tree.get_children():
            self.tree.delete(row)
        tipo = {0:"Administrador", 1:"Vendedor"}
        for user in users:
            self.tree.insert(
                '', 'end',
                values=(
                    user['id'],
                    user['username'],
                    user['fullname'],
                    user['phone'],
                    tipo[user['type']],
                    "Modificar",
                    "Borrar",
                )
            )


    
    def aplicar_filtros(self):
        opcion = self.tipo_var.get()
        if opcion == "0":
            users = self.users
        elif opcion == "1":
            users = [d for d in self.users if d.get("type") == 0]
        elif opcion == "2":
            users = [d for d in self.users if d.get("type") == 1]
        self.load_users_on_table(users)
        return
    
    def on_tree_click(self):
        return
    
    def process_input(self, event=None):
        code = self.entry.get().strip()
        if code:
            usuario = self.db.search("users", {"username": code, "fullname": code},["id", "username", "fullname", "phone", "type"], strict=False )
            self.load_users_on_table(usuario)

        return

