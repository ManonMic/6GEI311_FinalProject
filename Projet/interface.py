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
        self.lbl_img = tk.Label(self.root)
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
        bw_test = Image.fromarray(bytearray_img.astype('uint8'))
        self.image = ImageTk.PhotoImage(bw_test)
        self.lbl_img = tk.Label(self.root, image=self.image)
        self.lbl_img.pack()

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
