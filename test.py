import tkinter as tk
from ttkbootstrap import ttk

class App:
    def __init__(self, root):
        self.root = root

        right_frame = ttk.Frame(root)
        right_frame.pack(side="right", padx=10, pady=10)

        # Variable asociada al Entry
        self.efectivo_var = tk.StringVar()

        # Entry para efectivo
        self.efectivoEntry = ttk.Entry(right_frame, font=("Arial", 14), width=15, textvariable=self.efectivo_var)
        self.efectivoEntry.pack(pady=(5, 5), anchor="w")

        # Label para mostrar el cambio
        self.change_label = ttk.Label(right_frame, text="Cambio: $ 0.00", font=("Arial", 14), foreground="#BFBFBF", width=20)
        self.change_label.pack(anchor="w", pady=2)

        # Total de ejemplo (esto lo puedes calcular tú en tu método `actualizar_total`)
        self.total = 150.0

        # Detectar cambios en el Entry
        self.efectivo_var.trace_add("write", self.actualizar_cambio)

    def actualizar_cambio(self, *args):
        try:
            efectivo = float(self.efectivo_var.get())
            cambio = efectivo - self.total
            if cambio < 0:
                self.change_label.config(text="Cambio: $ 0.00", foreground="red")
            else:
                self.change_label.config(text=f"Cambio: $ {cambio:.2f}", foreground="#28A745")
        except ValueError:
            self.change_label.config(text="Cambio: $ 0.00", foreground="#BFBFBF")


root = tk.Tk()
app = App(root)
root.mainloop()
