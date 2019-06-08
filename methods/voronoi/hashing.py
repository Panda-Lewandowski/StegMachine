import hashlib
import numpy as np
from PIL import Image


def binarizate_by_average(elem, av):
    """Evaluates an element relative to average value
    
    :param elem: element to evaluate
    :type elem: int, float
    :param av:  average value
    :type av: int, float
    :return: 1 or 0
    :rtype: int, boolean
    """
    return 1 if elem >= av else 0


def get_sha256_hash(img_arr):
    """Returns sha256 hash
    
    :param img_arr: array to hash 
    :type img_arr: numpy array
    :return: hex string
    :rtype: str
    """
    return hashlib.sha256(img_arr).digest()


def get_md5_hash(img_arr):
    """Returns md5 hash
    
    :param img_arr: array to hash 
    :type img_arr: numpy array
    :return: hex string
    :rtype: str
    """
    return hashlib.md5(img_arr).digest()


def get_comparable_hash(img_arr):
    """Returns comparable hash of image
    
    :param img_arr: array to hash 
    :type img_arr: numpy array
    :return: hex string
    :rtype: str
    """
    img = Image.fromarray(img_arr)
    img = img.resize((8, 8), Image.ANTIALIAS)
    img = img.convert("L")
    average_color = img.resize((1, 1), Image.ANTIALIAS).getpixel((0, 0))
    img = np.array(img)
    bin_by_av = np.vectorize(binarizate_by_average)
    img = bin_by_av(img, average_color)
    hash = img.flatten()
    hash = "".join([str(elem) for elem in hash])
    return int(hash, 2).to_bytes(len(hash) // 8, byteorder='big')


if __name__ == "__main__":
    img = Image.open('test.jpg')
    img = np.array(img)
    print(get_comparable_hash(img))
    print(get_sha256_hash(img))
    print(get_md5_hash(img))
    
    
