import tkinter as tk
from zeroset import cv0
from PIL import ImageTk

images = cv0.glob("../data/", "*.*")


class ImageViewer():

    def __init__(self, window):
        self.canvas = tk.Canvas(window, width=2000, height=1000)
        self.canvas.grid(row=0, column=0)

        self.button = tk.Button(window, text="Next", command=self.on_button_clicked)
        self.button.grid(row=1, column=0)

        self.img = None
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW)
        self.image_idx = 0
        self.on_button_clicked()

    def on_button_clicked(self):
        self.img = ImageTk.PhotoImage(file=images[self.image_idx])
        width, height = self.img.width(), self.img.height()
        self.canvas.config(width=width, height=height)
        self.canvas.itemconfig(self.image_on_canvas, image=self.img)
        self.image_idx = (self.image_idx + 1) % len(images)
        pass


window = tk.Tk()
window.title("Image Viewer Sample")
ImageViewer(window)
window.mainloop()
