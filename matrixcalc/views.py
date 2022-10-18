import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog

import matrices

from matrixcalc.controllers import Adapter
import matrixcalc.dialogs as dialogs

class OperationListFrame(tk.Frame):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, *a, **kw)
        
        self.headers()
        
    def headers(self):
        self._otype = tk.Label(self, text="Type")
        self._otype.grid(row=0, column=0, sticky="nsew")
        
        self._data = tk.Label(self, text="Data")
        self._data.grid(row=0, column=1, sticky="nsew")
        
        self._value = tk.Label(self, text="Value")
        self._value.grid(row=0, column=2, sticky="nsew")
    
    def populate(self, data):
        data = reversed(data)
        i = 1
        for da in data:
            fn = self.rightclick_bind_fn(da)
            self._otype = tk.Label(self, text=da[1])
            self._otype.grid(row=i, column=0, sticky="nsew")
            self._otype.bind("<Button-3>", fn)
            
            self._data = tk.Label(self, text=da[2], anchor="e")
            self._data.grid(row=i, column=1, sticky="nsew")
            self._data.bind("<Button-3>", fn)
            
            self._value = tk.Label(self, text=str(da[3][:]), anchor="w")
            self._value.grid(row=i, column=2, sticky="nsew")
            self._value.bind("<Button-3>", fn)
            i += 1
    
    def rightclick_menu(self, data):
        popup = tk.Menu(tearoff=0)
        popup.add_command(label=f"Delete \"{data[1]} {data[0]}\"")
        
        return popup
    
    def rightclick_bind_fn(self, data):
        popup = self.rightclick_menu(data)
        def do_popup(event):
            # display the popup menu
            try:
                popup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                popup.grab_release()

        return do_popup

class MainWindow(tk.Tk):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        
        self.title("Matrix Pandit")
        
        if messagebox.askyesno("Workbook Creation", "Open an existing workbook? No will create a new one."):
            fname = filedialog.askopenfilename(filetypes=[("Matrices Workbook Files", "*.matrixpandit")])
        else:
            fname = filedialog.asksaveasfilename(filetypes=[("Matrices Workbook Files", "*.matrixpandit")], defaultextension=".matrixpandit")
        self.adapter = Adapter(fname)
        
        self.title(f"Matrix Pandit - {fname}")
        
        self._menu = tk.Menu(self, tearoff=0)
        self._file_menu = tk.Menu(self, tearoff=0)
        self._file_menu.add_command(label="Add Matrix", command=self.add_matrix)
        self._menu.add_cascade(label="File", menu=self._file_menu)
        self.config(menu=self._menu)
        
        self._frame = OperationListFrame(self)
        self._frame.grid(row=0, column=0, sticky="nsew")
        self._frame.populate(self.adapter.list_all())
    
    def add_matrix(self):
        varname = simpledialog.askstring("varname", "Enter Variable Name:")
        d = dialogs.MatrixEntryDialog(self)
        self.wait_window(d)
        m = d.matrix
        self.adapter.variable(varname, matrices.Matrix(m))
        self.refresh()
    
    def refresh(self):
        self._frame.destroy()
        self._frame = OperationListFrame(self)
        self._frame.grid(row=0, column=0, sticky="nsew")
        self._frame.populate(self.adapter.list_all())