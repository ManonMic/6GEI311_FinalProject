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
from skimage.color import label2rgb
from skimage.draw import polygon_perimeter, set_color
from skimage.filters import gaussian
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.segmentation import clear_border


def get_photo_offline(img):
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
    plt.imshow(arr, vmin=0, vmax=255)
    plt.tight_layout()
    plt.show()


def _to_np_array(byte_stream):
    arr = np.array(byte_stream)
    return arr.astype(np.int16)


def _resize_img(arr):
    """This ratio was chosen to get rid of the camera UI text"""
    return arr[130:1350, :]


def _open_as_bytestream(img):
    return Image.open(BytesIO(img))


def _to_grayscale(arr):
    img_bytes = _open_as_bytestream(arr)
    img_bytes = img_bytes.convert('L')
    return img_bytes


def _prepare_image(img):
    """Convert an image byte stream to grayscale into an array and applies a Gaussian blur to reduce noise """
    arr = _to_grayscale(img)
    arr = _to_np_array(arr)
    arr = _resize_img(arr)
    arr = gaussian(arr, sigma=3, preserve_range=True)
    arr = _to_np_array(arr)
    return arr


def _subtract_images(img1, img2):
    """Pixel per pixel differentiation and turning the result to black and white"""
    diff = np.abs(img2 - img1)
    diff = np.where(diff > 15, 255, 0)
    return diff


def process(img_arr):
    if len(img_arr) != 3:
        raise ValueError(
            "process requires an array of 3 images: img_arr parameter contains {} elements".format(len(img_arr))
        )

    # step 2 : Prepare images
    img1_prepared = _prepare_image(img_arr[0])
    img2_prepared = _prepare_image(img_arr[1])
    img3_prepared = _prepare_image(img_arr[2])

    # step 3 : resize a copy of the last image to use as the output
    output_img = _open_as_bytestream(img_arr[-1])
    output_img = _to_np_array(output_img)
    output_img = _resize_img(output_img)

    # step 4 : make a diff of each image vs its predecessor
    img_diff = _subtract_images(img3_prepared, img2_prepared)
    img_diff2 = _subtract_images(img3_prepared, img1_prepared)

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
