from geometry import Matrix, IndexedFace
import tkinter as tk
from math import cos, sin, radians


class Visualizer:
    HEIGHT = 600
    WIDTH = 600

    DEFAULT_SCALE = 200
    DEFAULT_ROTATION_X = 180
    DEFAULT_TRANSLATION_X = WIDTH / 2
    DEFAULT_TRANSLATION_Y = HEIGHT / 2

    verteces = []
    faces = []

    # orthogonal projection
    projection_matrix = Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
        ]
    )

    def __init__(self) -> None:
        self.SCALE = self.DEFAULT_SCALE
        self.ROTATION_X = self.DEFAULT_ROTATION_X
        self.ROTATION_Y = 0
        self.ROTATION_Z = 0
        self.TRANSLATION_X = self.DEFAULT_TRANSLATION_X / self.SCALE
        self.TRANSLATION_Y = self.DEFAULT_TRANSLATION_Y / self.SCALE

    def load_file(self, path: str):
        self.verteces = []
        self.faces = []

        with open(path) as file:
            line = file.readline()

            while line:
                line = [x.strip() for x in line.split(" ")]

                if line[0] == "v":
                    self.verteces.append(self._create_vertex(line))
                elif line[0] == "f":
                    self.faces.append(self._create_indexed_face(line))

                line = file.readline()

    def display(self, canvas: tk.Canvas):
        canvas.delete("all")

        # translate and scale points so that they display correctly on canvas
        translation_matrix = Matrix(
            [
                [1, 0, 0, self.TRANSLATION_X],
                [0, 1, 0, self.TRANSLATION_Y],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

        scale_matrix = Matrix(
            [
                [self.SCALE, 0, 0, 0],
                [0, self.SCALE, 0, 0],
                [0, 0, self.SCALE, 0],
                [0, 0, 0, 0],
            ]
        )

        self.ROTATION_Z = radians(self.ROTATION_Z)
        self.ROTATION_X = radians(self.ROTATION_X)
        self.ROTATION_Y = radians(self.ROTATION_Y)

        rotation_x_matrix = Matrix(
            [
                [1, 0, 0, 0],
                [0, cos(self.ROTATION_X), -sin(self.ROTATION_X), 0],
                [0, sin(self.ROTATION_X), cos(self.ROTATION_X), 0],
                [0, 0, 0, 1],
            ]
        )

        rotation_z_matrix = Matrix(
            [
                [cos(self.ROTATION_Z), -sin(self.ROTATION_Z), 0, 0],
                [sin(self.ROTATION_Z), cos(self.ROTATION_Z), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

        rotation_y_matrix = Matrix(
            [
                [cos(self.ROTATION_Y), 0, sin(self.ROTATION_Y), 0],
                [0, 1, 0, 0],
                [-sin(self.ROTATION_Y), 0, cos(self.ROTATION_Y), 0],
                [0, 0, 0, 1],
            ]
        )

        transformation_matrix = scale_matrix * self.projection_matrix
        transformation_matrix = transformation_matrix * translation_matrix
        transformation_matrix = transformation_matrix * rotation_x_matrix
        transformation_matrix = transformation_matrix * rotation_z_matrix
        transformation_matrix = transformation_matrix * rotation_y_matrix

        for face in self.faces:
            face.display(canvas, transformation_matrix)

    def _create_vertex(self, line: list) -> Matrix:
        return Matrix(
            [
                [float(line[1])],
                [float(line[2])],
                [float(line[3])],
                [float(line[4]) if len(line) > 4 else 1],
            ]
        )

    def _create_indexed_face(self, line: list) -> IndexedFace:
        verteces = [
            self.verteces[int(line[1]) - 1],
            self.verteces[int(line[2]) - 1],
            self.verteces[int(line[3]) - 1],
        ]
        indeces = [int(line[1]) - 1, int(line[2]) - 1, int(line[3]) - 1]

        return IndexedFace(verteces, indeces)
