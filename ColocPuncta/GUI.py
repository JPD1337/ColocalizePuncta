import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk

class ColocGUI:
    def  __init__(self):
        self.root = tk.Tk()
        self.root.title = "Colocalizing Toolkit"
        self.root.mainloop()

if __name__ == '__main__':
    gui = ColocGUI()