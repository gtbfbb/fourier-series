from tkinter import *
from tkinter import ttk
import math

class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.startx, self.starty = None, None
        self.lastx, self.lasty = None, None
        self.fx, self.fy = None, None

        self.bind("<Button-1>", self.start_shape)
        self.bind("<B1-Motion>", self.draw_shape)
        self.bind("<ButtonRelease-1>", self.finish_shape)

    def start_shape(self, event):
        self.startx, self.starty = event.x, event.y
        self.fx, self.fy = event.x, event.y
        self.distance = 0
        self.create_oval(self.startx - 2.5, self.starty - 2.5, self.startx + 2.5, self.starty + 2.5, fill="red", outline="red")

    def draw_shape(self, event):
        self.distance = math.sqrt((event.x - self.fx) ** 2 + (event.y - self.fy) ** 2)
        if (self.lastx is not None) and (self.lasty is not None):
            self.create_line(self.lastx, self.lasty, event.x, event.y, fill="black", width=5, smooth=True, capstyle=ROUND)

        if (self.distance > 10):
            self.create_oval(event.x - 4, event.y - 4, event.x + 4, event.y + 4, fill="red", outline="red")
            self.distance = 0
            self.fx, self.fy = event.x, event.y
        self.lastx, self.lasty = event.x, event.y

    def finish_shape(self, event):
        self.lastx, self.lasty = None, None
        self.distance = 10 * math.floor(math.sqrt((event.x - self.startx) ** 2 + (event.y - self.starty) ** 2) / 10)
        self.create_line(self.startx, self.starty, event.x, event.y, fill="black", width=5)
        s = 0

        while (s < 1):
            print(s)
            x = self.startx + (event.x - self.startx) * s
            y = self.starty + (event.y - self.starty) * s
            self.create_oval(x - 4, y - 4, x + 4, y + 4, fill="red", outline="red")
            s += 10/self.distance
            


            


root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("800x600")

sketch = Sketchpad(root)
sketch.grid(column=0, row=0, sticky=(N, W, E, S))

root.mainloop()