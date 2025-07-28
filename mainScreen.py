import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import LoginScreen as LG
import pages.ventas as VT
import pages.configuracion as CF
import pages.corte as CR
import pages.inventario as IN


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Punto de venta")
        self.root.state('zoomed')
        self.style = ttkb.Style(theme="minty")
        self.current_page = None
        self.logged_user = None  # NEW
        self.pages = {}
        self.initialize_ui()

    def initialize_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.current_page = None  # <-- Reset current page
        self.pages = {}  # <-- Reset page cache

        if self.logged_user:
            self.setup_navbar()

        self.main_content = ttk.Frame(self.root)
        self.main_content.pack(fill='both', expand=True, padx=10, pady=10)

        self.show_page("ventas")  # This will now be called unconditionally

    # ------------------- Navbar -------------------
    def setup_navbar(self):
        self.navbar = ttk.Frame(self.root, style='primary.TFrame', padding=(15, 10))
        self.navbar.pack(side='top', fill='x')

        ttk.Label(
            self.navbar, text="🛍 Punto de Venta",
            font=('Helvetica', 18, 'bold'),
            style='primary.Inverse.TLabel'
        ).pack(side='left', padx=(20, 30))

        space=340

        if self.logged_user['type'] == 0: 
            links = {
                "VENTAS": "ventas",
                "INVENTARIO": "inventario",
                "CORTE": "corte",
                "CONFIGURACION": "configuracion"
            }
            space =180
        elif  self.logged_user['type'] == 1:
            links = {
                "VENTAS": "ventas",
            }

        nav_links = ttk.Frame(self.navbar, style='primary.TFrame')
        nav_links.pack(side='left', padx=(space, 30))
            

        for text, page in links.items():
            self.create_nav_link(nav_links, text, lambda p=page: self.show_page(p))

        ttk.Label(self.navbar, style='primary.TFrame').pack(side='left', expand=True)

        # Separator and Logout
        sep_container = ttk.Frame(self.navbar, style='primary.TFrame')
        sep_container.pack(side='left', padx=(10, 20))
        ttk.Separator(sep_container, orient='vertical').pack(fill='y', expand=True)

        #just show the first 30 caracters of the number
        if len(self.logged_user['fullname']) < 25:
            name = self.logged_user['fullname']
        else:
            name = self.logged_user['fullname'][:25]
       
        ttk.Label(
            self.navbar,
            text=f"👤 {name}",
            font=('Helvetica', 12),
            style='primary.Inverse.TLabel'
        ).pack(side='left', padx=10)

        ttk.Button(self.navbar, text="Logout", command=self.logout, style='danger.TButton').pack(side='right', padx=10)

    def create_nav_link(self, parent, text, command):
        label = ttk.Label(parent, text=text, font=('Helvetica', 12), cursor="hand2", style='primary.Inverse.TLabel')
        label.pack(side='left', padx=15)
        label.bind("<Button-1>", lambda e: command())
        label.bind("<Enter>", lambda e: label.configure(foreground='#DDDDDD'))
        label.bind("<Leave>", lambda e: label.configure(foreground='white'))

    # ------------------- Page Navigation -------------------
    def show_page(self, page_name):
       
        # If already showing the desired page, do nothing
        #if self.current_page == page_name:
         #   return

        # Hide current page if any
        if self.current_page:
            self.clear_content()
            self.pages[self.current_page].pack_forget()

        # Create page if it doesn't exist yet
        if page_name not in self.pages:
            if page_name == "ventas":
                self.pages["ventas"] = VT.VentasPage(self.main_content)
            elif page_name == "inventario":
                self.pages["inventario"] = IN.InventarioPage(self.main_content)
            elif page_name == "corte":
                self.pages["corte"] = CR.CortePage(self.main_content)
            elif page_name == "configuracion":
                self.pages["configuracion"] = CF.ConfiguracionPage(self.main_content, self.style)
        


        # Show the new page
        self.pages[page_name].pack(fill='both', expand=True)
        self.current_page = page_name


    def clear_content(self):
        for widget in self.main_content.winfo_children():
            widget.pack_forget()

    # ------------------- Login -------------------
    def logout(self):
        """Return to login screen"""
        self.logged_user = None
        self.pages = {}  # ← clear cached pages
        self.current_page = None  # ← reset current page
        self.root.state('zoomed')
        LG.LoginScreen(self.root, self.after_login)


    
    def after_login(self, user_data):
        """Callback after successful login"""
        self.logged_user = user_data  # Save user info
        self.initialize_ui()
