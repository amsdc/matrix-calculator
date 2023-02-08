import re
import tkinter as tk
from tkinter import ttk
import sympy as sp
from PIL import Image, ImageTk
from io import BytesIO

LATEXTAG = re.compile(r"\[tex\](.*?)\[/tex\]", flags = re.DOTALL)
LATEXTAG2 = re.compile(r"\[tex\].*\[/tex\]", flags = re.DOTALL)

def latex_render(data, htmlcolor="FFFFFF"):
    expr = "$\displaystyle " + data + "$"

    #This creates a ByteIO stream and saves there the output of sympy.preview
    f = BytesIO()
    sp.preview(expr, euler = False, preamble = r"\documentclass{standalone}"
               r"\usepackage{pagecolor}"
               r"\usepackage{amsmath}"
               r"\definecolor{graybg}{HTML}{" + htmlcolor.upper() + "}"
               r"\pagecolor{graybg}"
               r"\begin{document}",
               viewer = "BytesIO", output = "png", outputbuffer=f)
    f.seek(0)
    # Open the image as if it were a file. This works only for .ps!
    img = Image.open(f)
    img.load()
    photo = ImageTk.PhotoImage(img)
    f.close()
    return photo

class LatexLabel(tk.Frame):
    def __init__(self, parent, text=None, *a, **kw):
        self._parent = parent
        super().__init__(parent, *a, **kw)
        if text: self.render(text)

    def clear(self):
        for cell in self.winfo_children():
            cell.destroy()

    def render(self, string):
        self.pics = []
        self.labels = []
        for i in LATEXTAG.findall(string):
            # string.replace(i, "\x00", 1)
            self.pics.append(latex_render(i))

        #string = LATEXTAG.sub("\x00", string)
        # r = string.split("\x00")
        r = LATEXTAG2.split(string)

        n = 0
        for i in range(len(r)):
            self.labels.append(tk.Label(self, text=r[i]))
            if i!=len(r)-1:
                self.labels.append(tk.Label(self, image=self.pics[i]))

        for i in self.labels:
            i.pack(side='left')
                
class LatexText(tk.Text):
    def __init__(self, parent, text=None, *a, **kw):
        self._parent = parent
        super().__init__(parent, *a, **kw)
        if text: self.render(text)

    def clear(self):
        self.delete("0.0", tk.END)

    def render(self, string):
        self.pics = []
        for i in LATEXTAG.findall(string):
            # string.replace(i, "\x00", 1)
            self.pics.append(latex_render(i))
        r = LATEXTAG2.split(string)

        n = 0
        for i in range(len(r)):
            self.insert(tk.END, r[i])
            if i!=len(r)-1:
                self.image_create(tk.END, image=self.pics[i])

        
    
