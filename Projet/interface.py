from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
import send_email
from threading import Thread, Event
from img_collector import get_photo
from image_processing import process, imshow, get_photo_offline


img_list = []
processed_outputs = []


def get_img():
    img_list.append(get_photo())


class GetImgThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self._stopped = event

    def stop(self):
        self._stopped.set()

    def run(self):
        while not self._stopped.wait(0.5):
            get_img()


class ProcessImgThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self._stopped = event

    def stop(self):
        self._stopped.set()

    def run(self):
        while not self._stopped.wait(0.01):
            if len(img_list) > 1:
                imgs = []
                for i in range(2):
                    imgs.append(img_list[i])
                for i in range(2):
                    del img_list[0]
                output_img, movement = process(imgs)
                processed_outputs.append((output_img, movement))


class Interface(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.running = True
        self.send_mail_enabled = False
        self.email_last_sent = None
        self.email_sending_cooldown_in_minutes = 10
        self.image = None

        self.byte_array_img = None
        self.image_display = tk.Label(master, image=self.image)

        self.email_notifications_recipient = tk.Label(master, text="Recipient email: ")
        default_email = "tr1013919@gmail.com"
        self.entry_mail_dest = tk.Entry(master)
        self.entry_mail_dest.insert(tk.END, default_email)
        self.button_running = tk.Button(master,
                                        text="Email notifications: Off",
                                        foreground="white",
                                        background="red",
                                        command=self.toggle_email_notifications)
        self.btn_send_test_notification = tk.Button(master, text="Send notification test",
                                                    command=lambda: self.send_email(test_email=True))

        master.geometry("1600x900")
        master.title("Surveillance camera")
        self.label = tk.Label()

        self.create_layout()
        self.updater()

    def create_layout(self):
        self.button_running.grid(row=0, column=2, columnspan=3, rowspan=1)
        self.email_notifications_recipient.grid(row=2, column=2, columnspan=10)
        self.entry_mail_dest.grid(row=2, column=3, columnspan=10)
        self.btn_send_test_notification.grid(row=4, column=2, columnspan=3, rowspan=1)
        self.image_display.grid(row=5, column=2, columnspan=2, rowspan=2)

    def is_running(self):
        return self.running

    def set_running(self, running):
        self.running = running

    def on_closing(self):
        self.master.destroy()
        self.set_running(False)

    def is_email_in_cooldown(self):
        now = datetime.now()
        if self.email_last_sent is None:
            self.email_last_sent = now
            return False
        elapsed_minutes = abs(now.second - self.email_last_sent.second) // 60
        return not (elapsed_minutes > self.email_sending_cooldown_in_minutes)

    def email_has_recipient(self):
        return len(self.entry_mail_dest.get()) > 0

    def can_send_an_email(self, test_email=False):
        has_recipient = self.email_has_recipient()
        if test_email:
            return has_recipient
        else:
            return self.send_mail_enabled and not self.is_email_in_cooldown() and has_recipient

    def send_email(self, test_email=False):
        if self.can_send_an_email(test_email=test_email):
            timestamp = self.email_last_sent.strftime('%d-%m-%Y %H:%M:%S')
            subject = "Movement detected!"
            body_msg = "There was movement detected on the camera.\n\nTimestamp: " \
                       + timestamp
            img = self.byte_array_img
            if test_email:
                subject = "Notification test"
                body_msg = "This is only a test. \n\n" \
                           "If you are receiving this email, the notification system works." \
                           "\n\nNo movements were detected."
                img = None
            else:
                self.email_last_sent = datetime.now()
            thread_send_email = Thread(target=lambda: send_email.send_email(dest=self.entry_mail_dest.get(),
                                                                            subject=subject,
                                                                            body=body_msg,
                                                                            image_bytestring=img))
            thread_send_email.start()

    def change_img(self, byte_array_img):
        if self.is_running():
            self.byte_array_img = byte_array_img
            converted_img = Image.fromarray(byte_array_img.astype('uint8'))
            resized = converted_img.resize((1600, 900), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(resized)
            self.image_display.configure(image=self.image)
            self.image_display.image = self.image
            self.master.update()

    def toggle_email_notifications(self):
        if len(self.entry_mail_dest.get()) > 0 and not self.send_mail_enabled:
            self.send_mail_enabled = True
            self.button_running['background'] = "green"
            self.button_running['text'] = "Email notifications: On"
            return
        self.send_mail_enabled = False
        self.button_running['background'] = "red"
        self.button_running['text'] = "Email notifications: Off"

    def updater(self):
        if self.running and len(processed_outputs) > 0:
            response = processed_outputs.pop(0)
            self.change_img(response[0])
            if response[1]:
                self.send_email()
        self.after(10, self.updater)


if __name__ == "__main__":
    root = tk.Tk()
    stop_flag = Event()
    img_thread = GetImgThread(stop_flag)
    img_thread.start()
    img_processing_thread = ProcessImgThread(stop_flag)
    img_processing_thread.start()
    gui = Interface(root)
    root.mainloop()
    img_thread.stop()
    img_processing_thread.stop()
