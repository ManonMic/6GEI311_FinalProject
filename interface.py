import tkinter as tk
from PIL import ImageTk
from PIL import Image
from io import BytesIO
import threading
from Projet import request


# class interface():
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.geometry("1600x900") 
#         self.root.title("Logiciel de surveillance")   
#         self.send_mail = True

#         self.img = request.get_photo()   

#         self.button_off = tk.Button(self.root, text="On", foreground="green", command=self.disable_send_mail)
#         self.button_off.pack()

#         self.button_close = tk.Button(self.root, text="Fermer", background="red", command=self.root.destroy)
#         self.button_close.pack()

#         self.image = Image.open(BytesIO(self.img))
#         self.image = ImageTk.PhotoImage(self.image)
#         self.label = tk.Label(self.root, image=self.image)
#         self.label.pack()

#         self.root.after(500, self.change_img)
#         self.root.mainloop()

#     def change_img(self):
#         self.image = request.get_photo()
#         self.image = Image.open(BytesIO(self.image))
#         self.image = ImageTk.PhotoImage(self.image)
#         self.label.configure(image=self.image)
#         self.label.image = self.image
#         self.root.after(500, self.change_img)

#     def disable_send_mail(self):
#         if self.send_mail:
#             self.send_mail = False
#             self.button_off['foreground'] = "red"
#             self.button_off['text'] = "Off"
#         else:
#             self.send_mail = True
#             self.button_off['foreground'] = "green"
#             self.button_off['text'] = "On"

# if __name__ == "__main__":
#     interface = interface()
#     print("yo")


class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.root = tk.Tk()
        self.root.geometry("1600x900") 
        self.root.title("Logiciel de surveillance")   
        self.send_mail = True

        self.img = request.get_photo()   

        self.button_off = tk.Button(self.root, text="On", foreground="green", command=self.disable_send_mail)
        self.button_off.pack()

        self.button_close = tk.Button(self.root, text="Fermer", background="red", command=self.root.quit)
        self.button_close.pack()

        self.image = Image.open(BytesIO(self.img))
        self.image = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(self.root, image=self.image)
        self.label.pack()

        self.root.after(500, self.change_img)
        self.root.mainloop()

    def callback(self):
        self.root.quit()

    def change_img(self):
        self.image = request.get_photo()
        self.image = Image.open(BytesIO(self.image))
        self.image = ImageTk.PhotoImage(self.image)
        self.label.configure(image=self.image)
        self.label.image = self.image
        self.root.after(500, self.change_img)

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
    app = App()
    print("yo")