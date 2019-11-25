import sys

from imageio import imread
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image
from scipy.linalg import norm
from scipy.ndimage import gaussian_filter as gaussian
import requests
from skimage.filters import gaussian
from skimage.color import label2rgb
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
        with open("data/image1.jpg", "rb") as image:
            f = image.read()
            b = bytearray(f)
    if img == 2:
        with open("data/image2.jpg", "rb") as image:
            f = image.read()
            b = bytearray(f)
    return b


def pre_treat_img(img):
    """Convert an image byte stream to grayscale into an array and applies a Gaussian blur to reduce noise """
    img_bytes = Image.open(BytesIO(img))
    img_grayscale = img_bytes.convert('L')
    arr = np.array(img_grayscale)
    arr = arr.astype(np.int16)
    return gaussian(arr, sigma=3)


if __name__ == "__main__":
    img1 = get_photo(1)
    img2 = get_photo(2)
    img1_treated = pre_treat_img(img1)
    img2_treated = pre_treat_img(img2)

    img_diff = np.abs(img2_treated - img1_treated)
    # bw_img = np.bitwise_and(img_diff, img_diff2)
    bw = closing(img_diff > 1, square(3))
    cleared = clear_border(bw)

    label_image = label(cleared)
    img_label_overlay = label2rgb(label_image, image=img1_treated)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(img_label_overlay)

    img_diff = img2_treated - img1_treated
    for region in regionprops(label_image):
        if region.area >= 100:
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                      fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)

    ax.set_axis_off()
    plt.tight_layout()
    plt.show()
