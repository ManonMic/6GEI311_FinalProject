import sys

from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter as gaussian
from skimage.color import label2rgb
from skimage.draw import polygon_perimeter, set_color
from skimage.filters import gaussian, threshold_otsu
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
    plt.imshow(arr, vmin=0, vmax=255, cmap='gray')
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
    min_img_number = 2
    if len(img_arr) != min_img_number:
        raise ValueError(
            "process requires an array of {} images: img_arr parameter contains {} elements"
            .format(min_img_number, len(img_arr))
        )

    img1_prepared = _prepare_image(img_arr[0])
    img2_prepared = _prepare_image(img_arr[1])

    output_img = _open_as_bytestream(img_arr[-1])
    output_img = _to_np_array(output_img)
    output_img = _resize_img(output_img)

    img_diff = _subtract_images(img1_prepared, img2_prepared)

    bw = closing(img_diff > 0, square(3))
    cleared = clear_border(bw)

    label_image = label(cleared)
    label2rgb(label=label_image, image=output_img)

    fig, ax = plt.subplots(figsize=(10, 6))
    movement = False
    regions = regionprops(label_image)
    if len(regions) > 0:
        minrow, mincol, maxrow, maxcol = regions[0].bbox
        for region in regions:
            if region.area >= 1000:
                movement = True
                minr, minc, maxr, maxc = region.bbox
                if minr < minrow:
                    minrow = minr
                if maxr > maxrow:
                    maxrow = maxr
                if minc < mincol:
                    mincol = minc
                if maxc > maxcol:
                    maxcol = maxr

        # sorry not sorry
        for i in range(3):
            rr, cc = polygon_perimeter([minrow - i, maxrow - i, maxrow - i, minrow - i],
                                       [mincol - i, mincol - i, maxcol - i, maxcol - i])

            set_color(output_img, (rr, cc), [255, 0, 0])
    return output_img, movement
