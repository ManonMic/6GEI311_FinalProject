import sys

# from ip_cam_image import get_photo

from imageio import imread
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image
from scipy.linalg import norm
from scipy.ndimage import gaussian_filter as gaussian
import requests
from skimage.color import label2rgb
from skimage.draw import polygon_perimeter, set_color
from skimage.filters import gaussian
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.segmentation import clear_border


def get_photo(img):
    """Get a photo from the IP camera"""
    # url = 'http://172.16.12.131/Streaming/channels/1/picture'
    # response = requests.get(url, auth=('admin', 'linux111'))
    # if response.status_code != 200:
    #     raise ConnectionError("Could not connect to the ip camera: {}".format(url))
    # return response.content

    if img == 1:
        with open("data/tester1.jpg", "rb") as image:
            f = image.read()
            b = bytearray(f)
    if img == 2:
        with open("data/tester2.jpg", "rb") as image:
            f = image.read()
            b = bytearray(f)
    if img == 3:
        with open("data/tester3.jpg", "rb") as image:
            f = image.read()
            b = bytearray(f)
    return b


def imshow(arr):
    plt.imshow(arr, cmap='gray', vmin=0, vmax=255)
    plt.tight_layout()
    plt.show()


class ImageProcessor:
    """Analyze a series of images and moving elements in it"""

    @staticmethod
    def _to_np_array(byte_stream):
        arr = np.array(byte_stream)
        return arr.astype(np.int16)

    @staticmethod
    def _resize_img(arr):
        """This ratio was chosen to get rid of the camera UI text"""
        return arr[130:1350, :]

    @staticmethod
    def _open_as_bytestream(img):
        return Image.open(BytesIO(img))

    def _to_grayscale(self, arr):
        img_bytes = self._open_as_bytestream(arr)
        img_bytes = img_bytes.convert('L')
        return img_bytes

    def _prepare_image(self, img):
        """Convert an image byte stream to grayscale into an array and applies a Gaussian blur to reduce noise """
        arr = self._to_grayscale(img)
        arr = self._to_np_array(arr)
        arr = self._resize_img(arr)
        arr = gaussian(arr, sigma=3, preserve_range=True)
        arr = self._to_np_array(arr)
        return arr

    @staticmethod
    def _subtract_images(img1, img2):
        """Pixel per pixel differentiation and turning the result to black and white"""
        diff = np.abs(img2 - img1)
        diff = np.where(diff > 15, 255, 0)
        return diff

    def process(self, img_arr):
        if len(img_arr) != 3:
            raise ValueError(
                "process requires an array of 3 images: img_arr parameter contains {} elements".format(len(img_arr))
            )

        # step 2 : Prepare images
        img1_prepared = self._prepare_image(img_arr[0])
        img2_prepared = self._prepare_image(img_arr[1])
        img3_prepared = self._prepare_image(img_arr[2])

        # step 3 : resize a copy of the last image to use as the output
        output_img = self._open_as_bytestream(img_arr[-1])
        output_img = self._to_np_array(output_img)
        output_img = self._resize_img(output_img)

        # step 4 : make a diff of each image vs its predecessor
        img_diff = self._subtract_images(img3_prepared, img2_prepared)
        imshow(img_diff)
        img_diff2 = self._subtract_images(img3_prepared, img1_prepared)
        imshow(img_diff2)

        # step 5: Do a bitwise comparison between the two differentiations
        bw_img = np.bitwise_and(img_diff2, img_diff)

        # step 6 : apply a threshold to remove gaps
        bw = closing(bw_img > 0, square(3))
        cleared = clear_border(bw)

        # step 7 : label image regions
        label_image = label(cleared)

        # step 8 : draw red box mask around large enough regions and apply to output image
        movement = False
        for region in regionprops(label_image):
            if region.area >= 200:
                movement = True
                minr, minc, maxr, maxc = region.bbox
                rr, cc = polygon_perimeter([minr-1, maxr-1, maxr-1, minr-1],
                                           [minc-1, minc-1, maxc-1, maxc-1])
                set_color(output_img, (rr, cc), [255, 0, 0])

        return output_img, movement


if __name__ == "__main__":
    # step 1 : acquire images
    img1 = get_photo(1)
    img2 = get_photo(2)
    img3 = get_photo(3)

    img_pr = ImageProcessor()
    result_img, someone_broke_in = img_pr.process([img1, img2, img3])

    imshow(result_img)
    if someone_broke_in:
        print("oh shoot someone broke in!")
