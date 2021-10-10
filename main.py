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
        self.canvas = tk.Canvas(canvas_frame, bg="white", height=self.visualizer.HEIGHT, width=self.visualizer.WIDTH)
        self.canvas.grid(row=0, column=0)
        canvas_frame.grid(row=0, column=0)

        # controls
        controls_wrapper_frame = tk.Frame(window)
        controls_wrapper_frame.grid(row=1, column=0)

        # rotation
        rotation_label = tk.Label(controls_wrapper_frame, text='Rotácia').grid(row=1, column=0)

        vcmd = (controls_wrapper_frame.register(self._digit_validation))

        self.rotation_x_input = tk.Entry(controls_wrapper_frame, validate='all', validatecommand=(vcmd, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.rotation_x_input.grid(row=2, column=0)
        self.rotation_y_input = tk.Entry(controls_wrapper_frame, validate='all', validatecommand=(vcmd, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.rotation_y_input.grid(row=3, column=0)
        self.rotation_z_input = tk.Entry(controls_wrapper_frame, validate='all', validatecommand=(vcmd, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.rotation_z_input.grid(row=4, column=0)

        scale_label = tk.Label(controls_wrapper_frame, text='Škálovanie').grid(row=1, column=1)
        self.scale_input = tk.Entry(controls_wrapper_frame, validate='all', validatecommand=(vcmd, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.scale_input.grid(row=2, column=1)

        translation_label = tk.Label(controls_wrapper_frame, text='Posun').grid(row=1, column=2)
        self.translation_x_input = tk.Entry(controls_wrapper_frame, validate='all', validatecommand=(vcmd, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.translation_x_input.grid(row=2, column=2)
        self.translation_y_input = tk.Entry(controls_wrapper_frame, validate='all', validatecommand=(vcmd, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.translation_y_input.grid(row=3, column=2)

        self._set_default_values()

        load_button = tk.Button(controls_wrapper_frame, text='Otvoriť', command=self._display_object).grid(row=5, column=0)
        load_button = tk.Button(controls_wrapper_frame, text='Resetovať', command=self._reset_object).grid(row=5, column=1)
        draw_button = tk.Button(controls_wrapper_frame, text='Prekresliť', command=self._redraw_object).grid(row=5, column=2)


    def _display_object(self, event=None):
        self.visualizer.load_file(filedialog.askopenfilename())
        self.visualizer.display(self.canvas)

    def _reset_object(self, event=None):
        self.visualizer.ROTATION_X = self.visualizer.DEFAULT_ROTATION_X
        self.visualizer.ROTATION_Y = 0
        self.visualizer.ROTATION_Z = 0

        self.visualizer.SCALE = self.visualizer.DEFAULT_SCALE

        self.visualizer.TRANSLATION_X = self.visualizer.DEFAULT_TRANSLATION_X / self.visualizer.SCALE
        self.visualizer.TRANSLATION_Y = self.visualizer.DEFAULT_TRANSLATION_Y / self.visualizer.SCALE

        self._set_default_values()

        self.visualizer.display(self.canvas)

    def _redraw_object(self, event=None):
        self.visualizer.ROTATION_X = float(self.rotation_x_input.get()) + self.visualizer.DEFAULT_ROTATION_X
        self.visualizer.ROTATION_Y = float(self.rotation_y_input.get())
        self.visualizer.ROTATION_Z = float(self.rotation_z_input.get())

        self.visualizer.SCALE = float(self.scale_input.get()) * self.visualizer.DEFAULT_SCALE

        self.visualizer.TRANSLATION_X = (float(self.translation_x_input.get()) + self.visualizer.DEFAULT_TRANSLATION_X) / self.visualizer.SCALE
        self.visualizer.TRANSLATION_Y = (float(self.translation_y_input.get()) + self.visualizer.DEFAULT_TRANSLATION_Y) / self.visualizer.SCALE

        self.visualizer.display(self.canvas)

    def _digit_validation(self, action, index, value_if_allowed,
                        prior_value, text, validation_type, trigger_type, widget_name):
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
        self.rotation_x_input.insert(0, '0')
        self.rotation_y_input.delete(0, END)
        self.rotation_y_input.insert(0, '0')
        self.rotation_z_input.delete(0, END)
        self.rotation_z_input.insert(0, '0')

        self.scale_input.delete(0, END)
        self.scale_input.insert(0, '1')

        self.translation_x_input.delete(0, END)
        self.translation_x_input.insert(0, '0')
        self.translation_y_input.delete(0, END)
        self.translation_y_input.insert(0, '0')

if __name__ == '__main__':
    ui = UserInterface()
    ui.display()