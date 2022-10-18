import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class MatrixEntryFrame(tk.Frame):
    def __init__(self, parent, m, n, *a, **kw):
        super().__init__(parent, *a, **kw)
        self._elements = []
        self._m, self._n = m, n

        for i in range(m):
            tk.Grid.rowconfigure(self, i, weight=1)
        for i in range(n):
            tk.Grid.columnconfigure(self, i, weight=1)

        for i in range(m):
            l = []
            for j in range(n):
                el = ttk.Entry(self, width=3)
                el.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)
                l.append(el)
            self._elements.append(l)

    def get_list(self):
        r=[]
        for i in range(self._m):
            l = []
            for j in range(self._n):
                el = float(self._elements[i][j].get())
                l.append(el)
            r.append(l)

        return r

class MatrixInfoFrame(tk.Frame):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, *a, **kw)

        self._prompt = tk.Label(self, text="Enter the order of matrix")
        self._prompt.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        self._m = ttk.Spinbox(self, width=3, from_=0, to=3)
        self._m.grid(row=1, column=0, padx=5, pady=5)
        self._m.set("0")

        self._x = tk.Label(self, text="\xd7") # * symbol
        self._x.grid(row=1, column=1, padx=5, pady=5)

        self._n = ttk.Spinbox(self, width=3, from_=0, to=3)
        self._n.grid(row=1, column=2, padx=5, pady=5)
        self._n.set("0")

    def get_order(self):
        try:
            return int(self._m.get()), int(self._n.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid Data format")

class MatrixEntryDialog(tk.Toplevel):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, *a, **kw)
        self.transient(parent)
        self.grab_set()

        
        self._title = tk.Label(self, text="Create Matrix")
        self._title.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # NOTICE: This frame is overwritten in self.getorder!! and is elastic
        # as below
        self._frame = MatrixInfoFrame(self)
        self._frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self._submit = ttk.Button(self, text="Enter Matrix", command=self.getorder)
        self._submit.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.rowconfigure(self, 1, weight=1)

    def getorder(self):
        m, n = self._frame.get_order()
        self._frame.destroy()

        self._title["text"] = "Enter the Matrix below:"
        self._submit["text"] = "Insert Martix"
        self._submit["command"] = self.getmatrix
        
        self._frame = MatrixEntryFrame(self, m, n)
        self._frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def getmatrix(self):
        self.matrix = self._frame.get_list()
        self.destroy()

if __name__ == "__main__":
    a = tk.Tk()
    b = MatrixEntryDialog(a)
    a.mainloop()

        

        

        
