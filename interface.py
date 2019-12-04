import tkinter as tk
from PIL import ImageTk
from PIL import Image
import requests
from io import BytesIO
import os
from datetime import datetime
import time


class interface():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1600x900")       
        self.photo_name_list = []

        self.button = tk.Button(self.root, text="Fermer", command=self.root.destroy)
        self.button.pack()

        #TODO: resize the image 
        self.image = Image.open(BytesIO(self.img))
        self.image = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(self.root, image=self.image)
        self.label.pack()

        self.root.after(500, self.change_img)
        # self.change_img()
        self.root.mainloop()

    def change_img(self):
        self.image = Image.open(BytesIO(self.image))
        self.image = ImageTk.PhotoImage(self.image)
        self.label.configure(image=self.image)
        self.label.image = self.image
        self.root.after(500, self.change_img)

if __name__ == "__main__":
    interface = interface()
