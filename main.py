import tkinter as tk
from tkinter import filedialog
from tkinter.constants import END

from visualizer import Visualizer


class UserInterface:
    def __init__(self) -> None:
        self.visualizer = Visualizer()

    def display(self) -> None:
        window = tk.Tk()
        self._setup_window(window)

        window.mainloop()

    def _setup_window(self, window) -> None:
        # canvas
        canvas_frame = tk.Frame(window)
        self.canvas = tk.Canvas(
            canvas_frame,
            bg="white",
            height=self.visualizer.HEIGHT,
            width=self.visualizer.WIDTH,
        )
        self.canvas.grid(row=0, column=0)
        canvas_frame.grid(row=0, column=0)

        # controls
        controls_wrapper_frame = tk.Frame(window)
        controls_wrapper_frame.grid(row=1, column=0)

        # rotation
        rotation_label = tk.Label(controls_wrapper_frame, text="Rotácia").grid(
            row=1, column=0
        )

        vcmd = controls_wrapper_frame.register(self._digit_validation)

        self.rotation_x_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.rotation_x_input.grid(row=2, column=0)
        self.rotation_y_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.rotation_y_input.grid(row=3, column=0)
        self.rotation_z_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.rotation_z_input.grid(row=4, column=0)

        # scale
        scale_label = tk.Label(controls_wrapper_frame, text="Škálovanie").grid(
            row=1, column=1
        )
        self.scale_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.scale_input.grid(row=2, column=1)

        # translation
        translation_label = tk.Label(controls_wrapper_frame, text="Posun").grid(
            row=1, column=2
        )
        self.translation_x_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.translation_x_input.grid(row=2, column=2)
        self.translation_y_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.translation_y_input.grid(row=3, column=2)
        self.translation_z_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.translation_z_input.grid(row=4, column=2)

        # light
        light_label = tk.Label(controls_wrapper_frame, text="Svetlo").grid(
            row=5, column=2
        )
        self.light_x_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.light_x_input.grid(row=6, column=2)
        self.light_y_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.light_y_input.grid(row=7, column=2)
        self.light_z_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.light_z_input.grid(row=8, column=2)

        # color
        color_label = tk.Label(controls_wrapper_frame, text="Farba RGB").grid(
            row=5, column=1
        )
        self.color_r_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.color_r_input.grid(row=6, column=1)
        self.color_g_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.color_g_input.grid(row=7, column=1)
        self.color_b_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.color_b_input.grid(row=8, column=1)

        # constants
        constants_label = tk.Label(
            controls_wrapper_frame, text="Konštanty Ka, Ks, Kd, h"
        ).grid(row=5, column=0)
        self.Ka_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.Ka_input.grid(row=6, column=0)
        self.Ks_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.Ks_input.grid(row=7, column=0)
        self.Kd_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.Kd_input.grid(row=8, column=0)
        self.h_input = tk.Entry(
            controls_wrapper_frame,
            validate="all",
            validatecommand=(vcmd, "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"),
        )
        self.h_input.grid(row=9, column=0)

        self._set_default_values()

        tk.Button(
            controls_wrapper_frame, text="Otvoriť", command=self._display_object
        ).grid(row=10, column=0)
        tk.Button(
            controls_wrapper_frame, text="Resetovať", command=self._reset_object
        ).grid(row=10, column=1)
        tk.Button(
            controls_wrapper_frame, text="Prekresliť", command=self._redraw_object
        ).grid(row=10, column=2)

    def _display_object(self, event=None):
        # Odkopirovat na inych systemoch ako na MacOS Monterey.
        # self.visualizer.load_file(filedialog.askopenfilename()) # MacOS monterey Python bug!
        self.visualizer.load_file("/Users/layo/Downloads/obj_files/bunny.obj")
        self.visualizer.display(self.canvas)

    def _reset_object(self, event=None):
        self.visualizer.ROTATION_X = self.visualizer.DEFAULT_ROTATION_X
        self.visualizer.ROTATION_Y = 0
        self.visualizer.ROTATION_Z = 0

        self.visualizer.SCALE = self.visualizer.DEFAULT_SCALE

        self.visualizer.TRANSLATION_X = (
            self.visualizer.DEFAULT_TRANSLATION_X / self.visualizer.SCALE
        )
        self.visualizer.TRANSLATION_Y = (
            self.visualizer.DEFAULT_TRANSLATION_Y / self.visualizer.SCALE
        )
        self.visualizer.TRANSLATION_Z = 0

        self._set_default_values()

        self.visualizer.display(self.canvas)

    def _redraw_object(self, event=None):
        self.visualizer.ROTATION_X = (
            float(self.rotation_x_input.get()) + self.visualizer.DEFAULT_ROTATION_X
        )
        self.visualizer.ROTATION_Y = float(self.rotation_y_input.get())
        self.visualizer.ROTATION_Z = float(self.rotation_z_input.get())

        self.visualizer.SCALE = (
            float(self.scale_input.get()) * self.visualizer.DEFAULT_SCALE
        )

        self.visualizer.TRANSLATION_X = (
            float(self.translation_x_input.get())
            + self.visualizer.DEFAULT_TRANSLATION_X
        ) / self.visualizer.SCALE
        self.visualizer.TRANSLATION_Y = (
            float(self.translation_y_input.get())
            + self.visualizer.DEFAULT_TRANSLATION_Y
        ) / self.visualizer.SCALE
        self.visualizer.TRANSLATION_Z = float(self.translation_z_input.get())

        self.visualizer.LIGHT_X = (
            float(self.light_x_input.get()) + self.visualizer.DEFAULT_LIGHT_X
        )
        self.visualizer.LIGHT_Y = (
            float(self.light_y_input.get()) + self.visualizer.DEFAULT_LIGHT_Y
        )
        self.visualizer.LIGHT_Z = (
            float(self.light_z_input.get()) + self.visualizer.DEFAULT_LIGHT_Z
        )

        self.visualizer.COLOR = (
            float(self.color_r_input.get()),
            float(self.color_g_input.get()),
            float(self.color_b_input.get()),
        )

        self.visualizer.Ks = float(self.Ks_input.get())
        self.visualizer.Ka = float(self.Ka_input.get())
        self.visualizer.Kd = float(self.Kd_input.get())
        self.visualizer.SHININESS = float(self.h_input.get())

        self.visualizer.display(self.canvas)

    def _digit_validation(
        self,
        action,
        index,
        value_if_allowed,
        prior_value,
        text,
        validation_type,
        trigger_type,
        widget_name,
    ):
        if value_if_allowed in ["", "-"]:
            return True

        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def _set_default_values(self):
        self.rotation_x_input.delete(0, END)
        self.rotation_x_input.insert(0, "0")
        self.rotation_y_input.delete(0, END)
        self.rotation_y_input.insert(0, "0")
        self.rotation_z_input.delete(0, END)
        self.rotation_z_input.insert(0, "0")

        self.scale_input.delete(0, END)
        self.scale_input.insert(0, "1")

        self.translation_x_input.delete(0, END)
        self.translation_x_input.insert(0, "0")
        self.translation_y_input.delete(0, END)
        self.translation_y_input.insert(0, "0")
        self.translation_z_input.delete(0, END)
        self.translation_z_input.insert(0, "0")

        self.light_x_input.delete(0, END)
        self.light_x_input.insert(0, "0")
        self.light_y_input.delete(0, END)
        self.light_y_input.insert(0, "0")
        self.light_z_input.delete(0, END)
        self.light_z_input.insert(0, "0")

        self.color_r_input.delete(0, END)
        self.color_r_input.insert(0, "99")
        self.color_g_input.delete(0, END)
        self.color_g_input.insert(0, "120")
        self.color_b_input.delete(0, END)
        self.color_b_input.insert(0, "220")

        self.Ka_input.delete(0, END)
        self.Ka_input.insert(0, "0.1")
        self.Ks_input.delete(0, END)
        self.Ks_input.insert(0, "0.5")
        self.Kd_input.delete(0, END)
        self.Kd_input.insert(0, "1")
        self.h_input.delete(0, END)
        self.h_input.insert(0, "1")


if __name__ == "__main__":
    ui = UserInterface()
    ui.display()
