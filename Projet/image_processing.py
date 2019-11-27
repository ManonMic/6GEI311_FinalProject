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


def imshow(arr):
    plt.imshow(arr, cmap='gray', vmin=0, vmax=255)
    plt.tight_layout()
    plt.show()


def get_photo(img):
    # """Get a photo from the IP camera"""
    # url = 'http://172.16.12.131/Streaming/channels/1/picture'
    # response = requests.get(url, auth=('admin', 'linux111'))
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


def to_np_array(byte_stream):
    arr = np.array(byte_stream)
    return arr.astype(np.int16)


def resize_img(arr):
    return arr[130:, :]


def to_grayscale(arr):
    img_bytes = Image.open(BytesIO(arr))
    return img_bytes.convert('L')


def pre_treat_img(img):
    """Convert an image byte stream to grayscale into an array and applies a Gaussian blur to reduce noise """
    arr = to_grayscale(img)
    arr = to_np_array(arr)
    arr = resize_img(arr)
    arr = gaussian(arr, sigma=3, preserve_range=True)
    arr = to_np_array(arr)
    return arr


if __name__ == "__main__":
    img1 = get_photo(1)
    img2 = get_photo(2)
    img3 = get_photo(3)
    img1_treated = pre_treat_img(img1)
    img2_treated = pre_treat_img(img2)
    img3_treated = pre_treat_img(img3)
    output_img = resize_img(to_np_array(Image.open(BytesIO(img3))))

    img_diff = np.abs(img3_treated - img2_treated)
    img_diff2 = np.abs(img3_treated - img1_treated)
    imshow(img_diff2)
    bw_img = np.bitwise_and(img_diff, img_diff2)
    bw = closing(bw_img > 10, square(3))
    cleared = clear_border(bw)

    label_image = label(cleared)
    for region in regionprops(label_image):
        if region.area >= 100:
            minr, minc, maxr, maxc = region.bbox
            rr, cc = polygon_perimeter([minr-1, maxr-1, maxr-1, minr-1],
                                       [minc-1, minc-1, maxc-1, maxc-1])
            set_color(output_img, (rr, cc), [255, 0, 0])
    imshow(output_img)
