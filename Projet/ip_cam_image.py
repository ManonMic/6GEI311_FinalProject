import requests
import shutil
import os
from datetime import datetime
import time


photo_name_list = []

def get_time():
    """Get time as a string : dd-mm-yy-hhmmss"""
    now = datetime.now()
    str_time = now.strftime("%m-%d-%Y-%H%M%S")
    return str_time


def create_dir_images():
    """Create a directory named 'images' in the current directory where images will be saved"""
    path = os.getcwd() + "/images"
    try:
        os.makedirs(path)
    except OSError:
        print("Creation of the directory "+ path + " failed")


def get_photo():
    """Get a photo from the IP camera"""       
    url = 'http://172.16.12.131/Streaming/channels/1/picture'
    reponse = requests.get(url, auth=('admin','linux111'))
    if reponse.status_code == 200:
        return reponse.content
    else:
        raise ValueError("Can't get any response")


def save_photo():
    """Save a photo .gif from the IP camera in the created directory 'images'. Its
    name is composed of the date and the hour of its capture"""
    photo = get_photo()
    if os.path.isdir("./images"):
        time = get_time()
        photo_name_list.append(time)
        location = "./images/" + time + ".gif"
        with open(location, "wb") as f:
            f.write(photo)
        return photo_name_list
    else:
        create_dir_images()
        save_photo()


def loop_saving_photos():
    """Infinite loop where we save a new picture in our images directory each 2 seconds"""
    while True:
        photo_name_list = save_photo()
        time.sleep(2)
        if len(photo_name_list) > 20:
            for photo in range(0,10):
                os.remove("./images/" + photo_name_list[photo] + ".gif")
            del photo_name_list[0:10]


if __name__ == "__main__":
    get_photo()
