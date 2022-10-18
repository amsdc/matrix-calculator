NUMERIC_CLASSES = (int, float, complex)
SH_MINOR = "m"
SH_COFACTOR = "cf"


class MatrixMultiplicationError(ArithmeticError):
    def __init__(self, x, y, z, w):
        super().__init__(f"Cannot multiply {x}*{y} and {z}*{w} matrix")


def matrix_rc(matrix):
    """Validate a list to be a matrix"""
    rows = len(matrix)
    cols = len(matrix[0])
    return rows, cols


def multiply(m1, m2):
    """Multiply two matrices m1 and m2"""
    if m1.cols == m2.rows:
        res = []
        for i in range(m1.rows):
            ro = []
            for j in range(m2.cols):
                el = 0
                for b in range(m1.cols):
                    el += m1[i:b] * m2[b:j]
                ro.append(el)
            res.append(ro)
        return Matrix(res)
    else:
        raise MatrixMultiplicationError(m1.rows, m1.cols, m2.rows, m2.cols)


def determinant(matrix):
    """Solve a n by n matrix using recursion"""
    n = matrix.rows

    if n == 1:
        return matrix[0:0]
    elif n == 2:
        return matrix[0:0] * matrix[1:1] - matrix[0:1] * matrix[1:0]
    else:
        sum_ = 0
        sign = -1
        for i in range(0, n):
            el = matrix[0:i]
            cfe = matrix.cofactor(0, i)
            sum_ += el * cfe

        return sum_

def adjoint(matrix):
    lst = []
    for i in range(matrix.rows):
        r = []
        for j in range(matrix.cols):
            r.append(matrix.cofactor(i, j))
        lst.append(r)

    return Matrix(lst).transpose()


class Matrix(object):
    def __init__(self, lst=[]):
        self.update(lst)

    def update(self, lst):
        """Update the matrix with a new list."""
        self.rows, self.cols = matrix_rc(lst)
        self._list = lst

    def __getitem__(self, item):
        if not isinstance(item, slice):
            raise TypeError("Matrix requires indices in slice notation.")
        else:
            if isinstance(item.start, int) and isinstance(item.stop, int):
                if item.step == SH_MINOR:
                    return self.minor(item.start, item.stop)
                elif item.step == SH_COFACTOR:
                    return self.cofactor(item.start, item.stop)
                else:
                    return self._list[item.start][item.stop]
            elif item.start == None and item.stop == None:
                return self._list
            else:
                raise TypeError("Invalid slice command")

    def minor(self, i, j):
        """Find the minor of a matrix.

        VERY IMPORTANT: i and j are zero-indexed!!!

        Args:
            matrix (list): The matrix
        """
        cf = []
        for _i in range(self.rows):
            if _i == i:
                continue
            cf.append([])
            for _j in range(self.cols):
                if _j == j:
                    continue
                cf[-1].append(self._list[_i][_j])

        return Matrix(cf)

    def cofactor(self, i, j):
        """Find the cofactor of the determinant"""
        return ((-1) ** (i + j)) * determinant(self.minor(i, j))

    def scalar_multiply(self, other):
        """Multiply the matrix by a scalar"""
        cf = []
        for _i in range(self.rows):
            ro = []
            for _j in range(self.cols):
                ro.append(self._list[_i][_j] * other)
            cf.append(ro)

        return Matrix(cf)

    def post_multiply(self, other):
        return multiply(self, other)

    def pre_multiply(self, other):
        return multiply(other, self)

    def transpose(self):
        new = []
        for i in range(self.cols):
            r = []
            for j in range(self.rows):
                r.append(self[j:i])
            new.append(r)

        return Matrix(new)

    def inverse(self):
        return (1/determinant(self))*adjoint(self)

    def __mul__(self, other):
        if type(other) in NUMERIC_CLASSES:
            return self.scalar_multiply(other)
        elif isinstance(other, Matrix):
            return self.post_multiply(other)

    def __rmul__(self, other):
        if type(other) in NUMERIC_CLASSES:
            return self.scalar_multiply(other)
        elif isinstance(other, Matrix):
            return self.pre_multiply(other)

    def __repr__(self):
        op = "<Matrix "
        for i in range(self.rows):
            for j in range(self.cols):
                op += str(self[i:j])
                op += " "
            op += "\n        "
        op += ">"
        return op
