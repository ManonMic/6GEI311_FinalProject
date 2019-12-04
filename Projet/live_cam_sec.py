from threading import Thread, Event

from request import get_photo
from image_processing import process, imshow
import interface


img_list = []


def get_img():
    img_list.append(get_photo())
    print("an image was acquired")


class GetImgThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(1):
            get_img()


if __name__ == "__main__":
    # interface = interface()
    stop_flag = Event()
    img_thread = GetImgThread(stop_flag)
    img_thread.start()
    while True:
        if len(img_list) > 3:
            imgs = []
            for i in range(3):
                imgs.append(img_list[i])
            del img_list[0]
            output_img, movement = process(imgs)
            imshow(output_img)
            # change image
