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
    DEFAULT_TRANSLATION_Z = -150

    COLOR = (99, 120, 220)

    DEFAULT_LIGHT_X = WIDTH / 2
    DEFAULT_LIGHT_Y = HEIGHT
    DEFAULT_LIGHT_Z = 0

    CAMERA_X = WIDTH / 2
    CAMERA_Y = HEIGHT / 2
    CAMERA_Z = -150

    SHININESS = 1
    Ka, Ks, Kd = 0.1, 0.1, 0.1

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
        self.TRANSLATION_Z = 0

        self.LIGHT_X, self.LIGHT_Y, self.LIGHT_Z = (
            self.DEFAULT_LIGHT_X,
            self.DEFAULT_LIGHT_Y,
            self.DEFAULT_LIGHT_Z,
        )
        self.light = Light(self.LIGHT_X, self.LIGHT_Y, self.LIGHT_Z)
        self.camera = Camera(self.CAMERA_X, self.CAMERA_Y, self.CAMERA_Z)

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
        self.light = Light(self.LIGHT_X, self.LIGHT_Y, self.LIGHT_Z)
        transformation_matrix = self._transform()

        for face in self.faces:
            face.reset()
            face.set_color(self.COLOR)
            face.set_transformation_matrix(transformation_matrix)
            face_center_of_gravity = face.center_of_gravity()
            # L, V vectors
            L, V = (
                face.verteces[0] - self.light.position,
                face.verteces[0] - self.camera.position,
            )

            L, V = L.normalize(), V.normalize()

            # normal
            N = face.get_normal().normalize()

            # backface culling - not very functional
            if V * N <= 0:
                continue

            light_camera_sum = L + V
            H = light_camera_sum.normalize()

            Is = (H * N) ** self.SHININESS
            Id = N * L

            I = self.Ka + (self.Kd * Id) + (self.Ks * Is)
            luminosity = I

            if luminosity > 1:
                luminosity = 1
            if luminosity < self.Ka:
                luminosity = self.Ka

            face.display(canvas, transformation_matrix, luminosity)

    def _transform(self) -> Matrix:
        # translate and scale points so that they display correctly on canvas
        translation_matrix = Matrix(
            [
                [1, 0, 0, self.TRANSLATION_X],
                [0, 1, 0, self.TRANSLATION_Y],
                [0, 0, 1, self.TRANSLATION_Z],
                [0, 0, 0, 1],
            ]
        )

        scale_matrix = Matrix(
            [
                [self.SCALE, 0, 0, 0],
                [0, self.SCALE, 0, 0],
                [0, 0, self.SCALE, 0],
                [0, 0, 0, 1],
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

        transformation_matrix = scale_matrix * translation_matrix
        transformation_matrix = transformation_matrix * rotation_x_matrix
        transformation_matrix = transformation_matrix * rotation_z_matrix
        transformation_matrix = transformation_matrix * rotation_y_matrix

        return transformation_matrix

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


class SpecialPoint:
    def __init__(self, x, y, z) -> None:
        self.position = Matrix(
            [
                [x],
                [y],
                [z],
                [1],
            ]
        )


class Light(SpecialPoint):
    pass


class Camera(SpecialPoint):
    pass
