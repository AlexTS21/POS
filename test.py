import tkinter as tk
from tkinter import ttk

root = tk.Tk()

ttk.Label(root, text="Name:").grid(row=0, column=0, sticky='e')
ttk.Entry(root).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(root, text="Password:").grid(row=1, column=0, sticky='e')
ttk.Entry(root, show="*").grid(row=1, column=1, padx=5, pady=5)

ttk.Button(root, text="Login").grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
