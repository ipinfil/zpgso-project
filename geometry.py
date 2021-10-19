import tkinter as tk


class Matrix:
    def __init__(self, matrix: list) -> None:
        if not len(matrix):
            raise ValueError("Can't make matrix from empty array.")

        self.matrix = matrix
        self.x_size = len(matrix[0])
        self.y_size = len(matrix)

    def __str__(self) -> str:
        return self.matrix.__str__()

    def __repr__(self) -> str:
        return self.matrix.__str__()

    def __mul__(self, other):
        if type(other) == Matrix:
            if self.x_size != other.y_size:
                raise ValueError("Cannot multiply matrice with wrong dimensions.")

            matrix = []

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
        self.indeces = indeces

    def __str__(self) -> str:
        return f"IndexedFace - {self.verteces}"

    def __repr__(self) -> str:
        return f"IndexedFace - {self.verteces}"

    def display(self, canvas: tk.Canvas, transform: Matrix):
        points = []

        for vertex in self.verteces:
            transformed = transform * vertex

            points.append(transformed[0][0])
            points.append(transformed[1][0])

        canvas.create_polygon(points, outline="#000000", fill="#FFFFFF")


if __name__ == "__main__":
    m = Matrix([[1, 0], [0, 1]])

    # print(m * 5)

    # m2 = Matrix([[0, 0],
    #             [0, 0]])

    # print(m * m2)

    m3 = Matrix([[2, 7], [9, 14]])

    print(m * m3)
