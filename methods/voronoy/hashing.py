import hashlib
import numpy as np
from PIL import Image


def binarizate_by_average(elem, av):
    return 1 if elem >= av else 0


def get_sha256_hash(img_arr):
    return hashlib.sha256(img_arr).hexdigest()


def get_md5_hash(img_arr):
    return hashlib.md5(img_arr).hexdigest()


def get_comparable_hash(img_arr):
    img = Image.fromarray(img_arr)
    img = img.resize((8, 8), Image.ANTIALIAS)
    img = img.convert("L")
    average_color = img.resize((1, 1), Image.ANTIALIAS).getpixel((0, 0))
    img = np.array(img)
    bin_by_av = np.vectorize(binarizate_by_average)
    img = bin_by_av(img, average_color)
    hash = img.flatten()
    return "".join([str(elem) for elem in hash])


if __name__ == "__main__":
    img = Image.open('test/3.png')
    img = np.array(img)
    print(get_comparable_hash(img))
    img = Image.open('test/4.png')
    img = np.array(img)
    print(get_comparable_hash(img))
    
