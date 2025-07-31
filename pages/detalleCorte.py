import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import ttk
from ttkbootstrap import Style
from scripts.database import DataBase

#0 pieza 1 caja 2 metro
class DetalleCortePage(ttkb.Frame):
    def __init__(self, parent, go_back_callback, corte, backTo):
        super().__init__(parent)
        self.db = DataBase("database.db")
        ttkb.Label(self, text="📇Detalle del corte", font=("Helvetica", 20, "bold"), bootstyle="primary").pack(anchor='nw', padx=30, pady=10)
        info_frame = ttkb.Frame(self)
        info_frame.pack(padx=50, pady=10, fill='x')
        info_frame.grid_columnconfigure(3, weight=1)
        ttkb.Button(info_frame, text=backTo, bootstyle="secondary",  command=go_back_callback).grid(row=0, column=3, sticky='e', pady=5)
        ttkb.Label(info_frame, text="Información:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w", padx=(0,5))
        
        
        for i, item in enumerate(corte.items()):
            key, atrib = item
            ttkb.Label(info_frame, text=f'{key}:').grid(row=i+2, column=1, sticky="w", padx=(45,5))
            ttkb.Label(info_frame, text=f'{atrib}').grid(row=i+2, column=2, sticky="w", padx=(0,5))
