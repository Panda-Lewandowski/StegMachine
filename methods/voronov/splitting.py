from PIL import Image
from math import sqrt, ceil


def split_to_workspace(img, n, z):
    a, b = img.size
    x = sqrt(a * b / n)
    w_x, h_x = int(a / ceil(a / x)), int(b / ceil(b / x))
    boxes = []
    mini_boxes = []
    for i in range(0, b, h_x):
        for j in range(0, a, w_x):
            boxes.append((j, i, j + w_x, i + h_x))
            mini_boxes.append((j + z, i + z, j + w_x - z, i + h_x - z))
    return boxes, mini_boxes


if __name__ == "__main__":
    split_to_workspace(Image.open('test.bmp'), 13, 20)