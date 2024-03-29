import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog

import matrices
import tk_latex

from matrixcalc.controllers import Adapter
import matrixcalc.dialogs as dialogs
from matrixcalc.helpers import list_to_tex

class OperationListFrame(tk.Frame):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, *a, **kw)
        self._parent = parent
        
        self.headers()
        
    def headers(self):
        self._otype = tk.Label(self, text="Type")
        self._otype.grid(row=1, column=0, sticky="nsew")
        
        self._data = tk.Label(self, text="Data")
        self._data.grid(row=1, column=1, sticky="nsew")
        
        self._value = tk.Label(self, text="Value")
        self._value.grid(row=1, column=2, sticky="nsew")
        
        self._displayframe = tk.Frame(self)
        self._displayframe.grid(row=0, column=0, columnspan=3, sticky="n")
    
    def populate(self, data):
        data = reversed(data)
        i = 2
        for da in data:
            fn = self.rightclick_bind_fn(da)
            self._otype = tk.Label(self, text=da[1])
            self._otype.grid(row=i, column=0, sticky="nsew")
            self._otype.bind("<Button-3>", fn)
            
            self._data = tk.Label(self, text=da[2], anchor="e")
            self._data.grid(row=i, column=1, sticky="nsew")
            self._data.bind("<Button-3>", fn)

            try:
                raise
                self._value = tk_latex.LatexLabel(self, text="[tex] "+ list_to_tex(da[3][:]) + " [/tex]")
            except:
                self._value = tk.Label(self, text=str(da[3][:]), anchor="w")
            self._value.grid(row=i, column=2, sticky="nsew")
            self._value.bind("<Button-3>", fn)
            i += 1
    
    def rightclick_menu(self, data):
        popup = tk.Menu(tearoff=0)
        popup.add_command(label=f"{data[1]} {data[0]}", state="disabled")
        popup.add_separator()
        popup.add_command(label=f"Delete")
        popup.add_separator()
        
        # Math operations
        math_menu = tk.Menu(tearoff=0)
        math_menu.add_command(label="Determinant", state=self._get_state_matrix(data[3]), command=lambda: self._op_det(data))
        math_menu.add_command(label="Adjoint", command=lambda: self._op_adjoint(data), state=self._get_state_matrix(data[3]))
        math_menu.add_command(label="Minor", state=self._get_state_matrix(data[3]))
        math_menu.add_command(label="Cofactor", state=self._get_state_matrix(data[3]))
        math_menu.add_command(label="Inverse", command=lambda: self._op_inverse(data), state=self._get_state_matrix(data[3]))
        popup.add_cascade(label="Transformations", menu=math_menu)
        
        oper_menu = tk.Menu(tearoff=0)
        oper_menu.add_command(label="Scalar Multiplication")
        oper_menu.add_command(label="Pre Multiply")
        oper_menu.add_command(label="Post Multiply")
        pwr_menu = tk.Menu(tearoff=0)
        pwr_menu.add_command(label="Square", command=lambda: self._op_power2(data))
        pwr_menu.add_command(label="Power N", command=lambda: self._op_powern(data))
        oper_menu.add_cascade(label="Powers", menu=pwr_menu)
        popup.add_cascade(label="Operations", menu=oper_menu)
        
        return popup
    
    def _get_state_matrix(self, matrix):
        if matrix.is_square:
            return None
        else:
            return "disabled"
    
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

    def _op_det(self, data):
        det = matrices.Matrix([[matrices.determinant(data[3])]])
        self.matdialog(det, f"Result of Determinant of '{data[2]}'")
    
    def _op_inverse(self, data):
        inv = data[3].inverse()
        self.matdialog(inv, f"Result of Inverse of '{data[2]}'")

    def _op_power2(self, data):
        inv = data[3]*data[3]
        self.matdialog(inv, f"Result of Power2 of '{data[2]}'")

    def _op_powern(self, data):
        times = simpledialog.askinteger("Times", "Power of")
        inv = data[3]
        for i in range(times-1):
            inv = inv * data[3]
        self.matdialog(inv, f"Result of Power{times} of '{data[2]}'")
    
    def _op_adjoint(self, data):
        inv = matrices.adjoint(data[3])
        self.matdialog(inv, f"Result of Adjoint of '{data[2]}'")

    def matdialog(self, lst, title):
        self._displayframe.destroy()
        self._displayframe = dialogs.MatrixDisplayFrame(self, data=lst, title=title, adapter=self._parent.adapter, refresh=self._parent.refresh, borderwidth=1, relief="solid")
        self._displayframe.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=2, pady=2)

class MainWindow(tk.Tk):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        
        self.title("Matrix Pandit")
        
        if messagebox.askyesno("Workbook Creation", "Open an existing workbook? No will create a new one."):
            fname = filedialog.askopenfilename(filetypes=[("Matrices Workbook Files", "*.matrixpandit")])
        else:
            fname = filedialog.asksaveasfilename(filetypes=[("Matrices Workbook Files", "*.matrixpandit")], defaultextension=".matrixpandit")
            print(repr(fname))
        self.adapter = Adapter(fname)
        
        self.title(f"Matrix Pandit - {fname}")
        
        self._menu = tk.Menu(self, tearoff=0)
        self._file_menu = tk.Menu(self, tearoff=0)
        self._file_menu.add_command(label="Add Matrix", command=self.add_matrix)
        self._file_menu.add_command(label="Refresh", command=self.refresh)
        self._file_menu.add_command(label="Quit", command=self.quit_)
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
    
    def quit_(self):
        self.adapter.connection.close()
        self.destroy()
