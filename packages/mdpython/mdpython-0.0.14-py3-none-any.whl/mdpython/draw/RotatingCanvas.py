import tkinter as tk
import math


class RotatingCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.angle = 0
        self.is_rotating = False
        self.points = []
        self.cur_pt = []

        self.bind("<ButtonPress-1>", self.start_rotation)
        self.bind("<ButtonRelease-1>", self.stop_rotation)
        self.bind("<Motion>", self.draw_point)

        self.rotate()

    def start_rotation(self, event):
        self.is_rotating = True
        self.cur_pt = (event.x, event.y, 0)

    def stop_rotation(self, event):
        self.is_rotating = False

    def draw_point(self, event):
        if self.is_rotating:
            self.cur_pt = (event.x, event.y, 0)

    def rotate(self):
        self.angle = (self.angle - 1) % 360
        if self.is_rotating:
            x,y,angle = self.cur_pt
            rad = math.radians(angle)
            cos_val = math.cos(rad)
            sin_val = math.sin(rad)
            x_rot = cos_val * (x - 200) - sin_val * (y - 200) + 200
            y_rot = sin_val * (x - 200) + cos_val * (y - 200) + 200
            self.points.append([x_rot, y_rot, self.angle])


        self.delete('all')
        for x,y,angl in self.points:
            ref_angle = (self.angle - angl) % 360
            rad = math.radians(ref_angle)
            cos_val = math.cos(rad)
            sin_val = math.sin(rad)
            x_rot = cos_val * (x - 200) - sin_val * (y - 200) + 200
            y_rot = sin_val * (x - 200) + cos_val * (y - 200) + 200
            self.create_oval(x_rot - 5, y_rot - 5, x_rot + 5, y_rot + 5,
                             fill="red",outline="red")

        self.after(10, self.rotate)  # Update every 50ms


root = tk.Tk()
root.title("Rotating Canvas")

canvas = RotatingCanvas(root, width=400, height=400, bg="white")
canvas.pack()

root.mainloop()
