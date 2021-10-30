import tkinter as tk
from math import sqrt
from copy import deepcopy


class Matrix:
    def __init__(self, matrix: list) -> None:
        if not len(matrix):
            raise ValueError("Can't make matrix from empty array.")

        self.matrix = matrix
        self.x_size = len(matrix[0])
        self.y_size = len(matrix)

    def vector_length(self):
        if any([len(x) > 1 for x in self.matrix]):
            raise ValueError("This is not a vector.")

        return sqrt(sum([sum(x) ** 2 for x in self.matrix[:-1]]))

    def shape(self):
        return (self.x_size, self.y_size)

    def __str__(self) -> str:
        return self.matrix.__str__()

    def __repr__(self) -> str:
        return self.matrix.__str__()

    def __add__(self, other):
        if self.shape() != other.shape():
            return ValueError("Matrices do not share the same shape.")

        matrix = []
        for row in range(self.y_size):
            matrix.append([])
            for col in range(self.x_size):
                matrix[-1].append(self.matrix[row][col] + other[row][col])

        return Matrix(matrix)

    def __sub__(self, other):
        if self.shape() != other.shape():
            return ValueError("Matrices do not share the same shape.")

        matrix = []
        for row in range(self.y_size):
            matrix.append([])
            for col in range(self.x_size):
                matrix[-1].append(self.matrix[row][col] - other[row][col])

        return Matrix(matrix)

    def __truediv__(self, other):
        if type(other) == Matrix:
            raise ValueError("Cannot divide matrices.")

        matrix = []
        for row in range(self.y_size):
            matrix.append([])
            for col in range(self.x_size):
                matrix[-1].append(self.matrix[row][col] / other)

        return Matrix(matrix)

    def __mul__(self, other):
        if type(other) == Matrix:
            if self.x_size != other.y_size and self.x_size != 1 and other.x_size != 1:
                raise ValueError("Cannot multiply matrice with wrong dimensions.")

            matrix = []

            if self.x_size == 1 and other.x_size == 1:
                tmp = 0

                for x in range(3):
                    tmp += self.matrix[x][0] * other.matrix[x][0]

                return tmp

            for row in range(self.y_size):
                matrix.append([])
                for col in range(other.x_size):
                    matrix[-1].append(0)

            for row in range(self.y_size):
                for col in range(other.x_size):
                    for i in range(other.y_size):
                        matrix[row][col] += self.matrix[row][i] * other.matrix[i][col]

            return Matrix(matrix)

        elif type(other) in (int, float):
            matrix = Matrix(list(self.matrix))

            for row in range(self.y_size):
                for col in range(self.x_size):
                    matrix.matrix[row][col] *= other

            return matrix

        raise NotImplementedError()

    def __getitem__(self, key):
        return self.matrix[key]


class IndexedFace:
    verteces = None
    indeces = None

    def __init__(self, verteces: list, indeces: list) -> None:
        self.verteces = verteces
        self.original_verteces = deepcopy(verteces)
        self.indeces = indeces

    def __str__(self) -> str:
        return f"IndexedFace - {self.verteces}"

    def __repr__(self) -> str:
        return f"IndexedFace - {self.verteces}"

    def set_color(self, color):
        self.color = color

    def set_transformation_matrix(self, transformation_matrix):
        self.transform = transformation_matrix

        for i in range(len(self.verteces)):
            self.verteces[i] = self.transform * self.verteces[i]

    def reset(self):
        self.verteces = deepcopy(self.original_verteces)

    def display(self, canvas: tk.Canvas, transform: Matrix, luminosity: float):
        points = []

        for vertex in self.verteces:
            points.append(vertex[0][0])
            points.append(vertex[1][0])

        color = (int(x * luminosity) for x in self.color)
        hexcode = "#"

        for value in color:
            hexvalue = hex(value)

            if hexvalue[0] == "-":
                hexvalue = hexvalue[3:]
            else:
                hexvalue = hexvalue[2:]

            if len(hexvalue) == 1:
                hexvalue = "0" + hexvalue

            hexcode += hexvalue

        canvas.create_polygon(points, fill=hexcode)

    def center_of_gravity(self):
        matrix = []

        for row in range(4):
            matrix.append([sum([x[row][0] for x in self.verteces]) / 3])

        return Matrix(matrix)

    def get_normal(self):
        v1 = self.verteces[1] - self.verteces[0]
        v2 = self.verteces[2] - self.verteces[1]

        Cx = v1[1][0] * v2[2][0] - v1[2][0] * v2[1][0]
        Cy = v1[2][0] * v2[0][0] - v1[0][0] * v2[2][0]
        Cz = v1[0][0] * v2[1][0] - v1[1][0] * v2[0][0]

        return Matrix([[Cx], [Cy], [Cz]])


if __name__ == "__main__":
    # m = Matrix([[1, 0], [0, 1]])

    # print(m * 5)

    # m2 = Matrix([[0, 0],
    #             [0, 0]])

    # print(m * m2)

    # m3 = Matrix([[2, 7], [9, 14]])

    # print(m * m3)

    v1 = Matrix([[1], [2], [3]])
    v2 = Matrix([[2], [3], [4]])

    print(v1 * v2)
