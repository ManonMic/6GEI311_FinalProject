import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import threading
import send_email
import time


class Interface(threading.Thread):
    def __init__(self):
        self.root = tk.Tk()
        self.send_mail = True
        # self.img = bytearray()
        self.image = bytearray()
        # self.image_bytestring = Image.open(BytesIO(self.img))
        self.button_off = tk.Button(self.root, text="On", foreground="green", command=self.disable_send_mail)
        self.button_close = tk.Button(self.root, text="Fermer", background="red", command=self.root.quit)
        self.button_send = tk.Button(self.root, text="Envoyer mail", command=self.send_mail_test)

        self.root.geometry("1600x900")
        self.root.title("Logiciel de surveillance")
        self.button_off.pack()
        self.button_close.pack()
        self.label = tk.Label()

        self.button_send.pack()
        threading.Thread.__init__(self)
        self.start()

    def send_mail_test (self):    
        send_email.send_email(dest="manon190.mm@gmail.com", subject="Détection personne",
                          body="Reeeeee!", image_bytestring=self.image_bytestring)

    def change_img(self, bytearray_img):
        self.image = bytearray_img
        # self.image = Image.open(BytesIO(self.image))
        # self.image = self.image.resize((1600, 900), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image=Image.fromarray(bytearray_img))

        # self.label.configure(image=self.image)
        # self.label.image = self.image
        # self.root.after(500, self.change_img)
        self.canvas = tk.Canvas(self.root, width=1600, height=900)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        self.root.mainloop()

    def disable_send_mail(self):
        if self.send_mail:
            self.send_mail = False
            self.button_off['foreground'] = "red"
            self.button_off['text'] = "Off"
        else:
            self.send_mail = True
            self.button_off['foreground'] = "green"
            self.button_off['text'] = "On"


if __name__ == "__main__":
    gui = Interface()
