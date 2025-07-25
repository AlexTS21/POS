import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb

def main():
    try:
        root = ttkb.Window(themename="darkly")
        root.title("TTK Bootstrap Navbar")
        root.geometry("800x600")
        
        # Simple label to verify window creation
        test_label = ttkb.Label(root, text="Window created successfully!", bootstyle="danger")
        test_label.pack(pady=50)
        
        # Add your navbar code here...
        
        root.mainloop()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        input("Press Enter to close...")  # Keeps window open to see error

if __name__ == "__main__":
    main()