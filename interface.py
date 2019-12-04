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
        self.img = self.get_photo()
        self.photo_name_list = []

        self.button = tk.Button(self.root, text="Fermer", command=self.root.destroy)
        self.button.pack()

        #TODO: resize the image 
        self.image = Image.open(BytesIO(self.img))
        self.image = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(self.root, image=self.image)
        self.label.pack()

        self.loop_saving_photos()
        self.root.after(500, self.change_img)
        # self.change_img()
        self.root.mainloop()

    @staticmethod
    def get_photo():
        """Get a photo from the IP camera"""       
        url = 'http://172.16.12.131/Streaming/channels/1/picture'
        reponse = requests.get(url, auth=('admin','linux111'))
        if reponse.status_code == 200:
            return reponse.content
        else:
            raise ValueError("Can't get any response")

    @staticmethod
    def create_dir_images():
        """Create a directory named 'images' in the current directory where images will be saved"""
        path = os.getcwd() + "/images"
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory "+ path + " failed")

    @staticmethod
    def get_time():
        """Get time as a string : dd-mm-yy-hhmmss"""
        now = datetime.now()
        str_time = now.strftime("%m-%d-%Y-%H%M%S")
        return str_time

    def change_img(self):
        self.image = self.get_photo()
        self.image = Image.open(BytesIO(self.image))
        self.image = ImageTk.PhotoImage(self.image)
        self.label.configure(image=self.image)
        self.label.image = self.image
        self.root.after(500, self.change_img)

    def save_photo(self):
        """Save a photo .gif from the IP camera in the created directory 'images'. Its
        name is composed of the date and the hour of its capture"""
        photo = self.get_photo()
        if os.path.isdir("./images"):
            time = self.get_time()
            self.photo_name_list.append(time)
            location = "./images/" + time + ".jpg"
            with open(location, "wb") as f:
                f.write(photo)
            return self.photo_name_list
        else:
            self.create_dir_images()
            self.save_photo()

    def loop_saving_photos(self):
        """Infinite loop where we save a new picture in our images directory each 2 seconds"""
        self.photo_name_list = self.save_photo()
        time.sleep(2)
        if len(self.photo_name_list) > 20:
            for photo in range(0,10):
                os.remove("./images/" + self.photo_name_list[photo] + ".jpg")
            del self.photo_name_list[0:10]
        self.root.after(500, self.loop_saving_photos)

if __name__ == "__main__":
    interface = interface()
