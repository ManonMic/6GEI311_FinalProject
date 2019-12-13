import datetime
import time
import tkinter as tk
from PIL import Image, ImageTk
import threading
import send_email
from threading import Thread, Event
from img_collector import get_photo
from image_processing import process, imshow, get_photo_offline


img_list = []


def get_img():
    img_list.append(get_photo())


class GetImgThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self._stopped = event

    def stop(self):
        self._stopped.set()

    def run(self):
        while not self._stopped.wait(1):
            get_img()


class Interface:
    def __init__(self):
        self.root = tk.Tk()
        self.running = True
        self.send_mail_enabled = True
        self.email_last_sent = 0
        self.email_sending_cooldown = 10
        self.image = None

        self.bytearray_img = None
        self.image_display = tk.Label(self.root, image=self.image)
        self.button_running = tk.Button(self.root, text="On", foreground="green", command=self.disable_send_mail)
        self.button_close = tk.Button(self.root, text="Fermer", background="red", command=self.root.quit)
        self.button_send = tk.Button(self.root, text="Envoyer mail", command=self.send_mail)
        self.label_get_email = tk.Label(self.root, text="Email du destinataire = ")
        self.entry_mail_dest = tk.Entry(self.root)

        self.root.geometry("1600x900")
        self.root.title("Logiciel de surveillance")
        self.label = tk.Label()

        self.create_layout()

    def create_layout(self):
        self.button_running.grid(row=0, column=2, columnspan=3, rowspan=1)
        self.button_close.grid(row=1, column=2, columnspan=3, rowspan=1)
        self.label_get_email.grid(row=2, column=2, columnspan=3, rowspan=1)
        self.entry_mail_dest.grid(row=3, column=2, columnspan=3, rowspan=1)
        self.button_send.grid(row=4, column=2, columnspan=3, rowspan=1)
        self.image_display.grid(row=5, column=2, columnspan=2, rowspan=2)

    def is_running(self):
        return self.running

    def set_running(self, running):
        self.running = running

    def on_closing(self):
        self.root.destroy()
        self.set_running(False)

    def is_email_in_cooldown(self):
        now = time.time()
        elapsed = (now - self.email_last_sent) / (3600 * 60)
        return not (elapsed > self.email_sending_cooldown)

    def send_mail(self):
            self.email_last_sent = time.time()
            timestamp = datetime.datetime.fromtimestamp(self.email_last_sent).strftime('%d-%m-%Y %H:%M:%S')
            body_msg = "Ce message est pour vous indiquer qu'un mouvement a été détecté sur votre caméra timestamp: " \
                       + timestamp
            send_email.send_email(dest=self.entry_mail_dest.get(), subject="Détection de mouvement",
                              body=body_msg, image_bytestring=self.bytearray_img)

    def change_img(self, bytearray_img):
        if self.is_running():
            self.bytearray_img = bytearray_img
            converted_img = Image.fromarray(bytearray_img.astype('uint8'))
            resized = converted_img.resize((1600, 900), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(resized)
            self.image_display.configure(image=self.image)
            self.image_display.image = self.image
            self.root.update()

    def disable_send_mail(self):
        if self.send_mail_enabled:
            self.send_mail_enabled = False
            self.button_running['foreground'] = "red"
            self.button_running['text'] = "Off"
        else:
            self.send_mail_enabled = True
            self.button_running['foreground'] = "green"
            self.button_running['text'] = "On"


if __name__ == "__main__":
    gui = Interface()
    stop_flag = Event()
    img_thread = GetImgThread(stop_flag)
    img_thread.start()
    while gui.is_running():
        if len(img_list) > 1:
            imgs = []
            for i in range(2):
                imgs.append(img_list[i])
            del img_list[0]
            output_img, movement = process(imgs)
            gui.change_img(output_img)
            if movement and gui.send_mail_enabled and not gui.is_email_in_cooldown():
                gui.send_mail()

    img_thread.stop()
    # TODO: Regarder comment faire en sorte que l'interface ne soit pas bloqué par les autres actions
    # TODO: Arrêter le thread d'acquisition des images lorsque l'interface est fermé
