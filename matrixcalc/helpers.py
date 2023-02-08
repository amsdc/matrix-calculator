def list_to_tex(lst):
    st = "\\begin{bmatrix}\n"
    for i in lst:
        st += " & ".join(map(str, i)) + "\\\\\n"
    st += "\\end{bmatrix}"
    return st
