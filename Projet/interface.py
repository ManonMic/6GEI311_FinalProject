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
processed_outputs = []
img_changed_flag = False


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


class ProcessImgThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self._stopped = event

    def stop(self):
        self._stopped.set()

    def run(self):
        while not self._stopped.wait(0.5):
            if len(img_list) > 1:
                imgs = []
                for i in range(2):
                    imgs.append(img_list[i])
                for i in range(2):
                    del img_list[0]
                img_changed_flag = False
                output_img, movement = process(imgs)
                processed_outputs.append((output_img, movement))


class Interface(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.running = True
        self.send_mail_enabled = True
        self.email_last_sent = 0
        self.email_sending_cooldown = 10
        self.image = None

        self.bytearray_img = None
        self.image_display = tk.Label(master, image=self.image)
        self.button_running = tk.Button(master, text="On", foreground="green", command=self.disable_send_mail)
        self.button_close = tk.Button(master, text="Fermer", background="red", command=self.master.quit)
        self.button_send = tk.Button(master, text="Envoyer mail", command=self.send_mail)
        self.label_get_email = tk.Label(master, text="Email du destinataire = ")
        self.entry_mail_dest = tk.Entry(master)

        master.geometry("1600x900")
        master.title("Logiciel de surveillance")
        self.label = tk.Label()

        self.create_layout()
        self.updater()

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
        self.master.destroy()
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
            self.master.update()

    def disable_send_mail(self):
        if self.send_mail_enabled:
            self.send_mail_enabled = False
            self.button_running['foreground'] = "red"
            self.button_running['text'] = "Off"
        else:
            self.send_mail_enabled = True
            self.button_running['foreground'] = "green"
            self.button_running['text'] = "On"

    def updater(self):
        if self.running and len(processed_outputs) > 0:
            response = processed_outputs.pop(0)
            self.change_img(response[0])
            if response[1] and self.send_mail_enabled and not self.is_email_in_cooldown():
                self.send_mail()
        self.after(200, self.updater)


if __name__ == "__main__":
    root = tk.Tk()
    stop_flag = Event()
    img_thread = GetImgThread(stop_flag)
    img_thread.start()
    img_processing_thread = ProcessImgThread(stop_flag)
    img_processing_thread.start()
    gui = Interface(root)
    root.mainloop()
    # while gui.is_running():
    #     if img_changed_flag is False and len(processed_imgs) > 0:
    #         img = processed_imgs.pop(0)
    #         gui.change_img(img)
    #         img_changed_flag = True
    #     gui.updater()
    # if len(img_list) > 1:
    #     imgs = []
    #     for i in range(2):
    #         imgs.append(img_list[i])
    #     del img_list[0]
    #     output_img, movement = process(imgs)
    #     gui.change_img(output_img)
    #     if movement and gui.send_mail_enabled and not gui.is_email_in_cooldown():
    #         gui.send_mail()

    img_thread.stop()
    # TODO: Regarder comment faire en sorte que l'interface ne soit pas bloqué par les autres actions
    # TODO: Arrêter le thread d'acquisition des images lorsque l'interface est fermé
