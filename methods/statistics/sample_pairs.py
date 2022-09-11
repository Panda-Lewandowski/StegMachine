""" 
This module contains the required functions to implement 
Sample pairs attack method.
"""

from PIL import Image
from math import sqrt

def spa_test(img):
    """Using the Sample pairs method
    
    :param img: Image name
    """
    height, width = img.size

    if width % 2  == 1:
        width -= 1
    if height % 2  == 1:
        height -= 1


    average = 0.0

    r, g, b = img.split()[:3]

    average = analyze(r.load(), height, width)
    average += analyze(g.load(), height, width, channel='g')
    average += analyze(b.load(), height, width, channel='b')

    average = average / 3.0
    average = abs(average)
    if average > 1:
        return 1
    else:
        return average


def analyze(pix, h, w, channel='r'):
    """Container analysis for steganography

    :param pix: Image pixels
    :param h: Image height
    :param w: Image width
    :param channel: One of three possible RGB channels. Set 'r' for red, 'g' for green, 'b' for blue
    """
    P = 0 
    X = 0 
    Y = 0 
    Z = 0
    W = 0

    for i in range(0, h - 1):
        for j in range(0, w - 1, 2):
            u = pix[i, j]
            v = pix[i + 1, j]

            if (u >> 1 == v >> 1) and ((v & 0x1) != (u & 0x1)):
                W += 1

            if u == v:
                Z += 1

            # if lsb(v) = 0 & u < v OR lsb(v) = 1 & u > v
            if (v == (v >> 1) << 1) and (u < v) or (v != (v >> 1) << 1) and (u > v):
                X += 1

            # vice versa
            if (v == (v >> 1) << 1) and (u > v) or (v != (v >> 1) << 1) and (u < v):
                Y += 1
            
            P += 1 

    for i in range(0, h - 1, 2):
        for j in range(0, w - 1):
            u = pix[i, j]
            v = pix[i, j + 1]

            if (u >> 1 == v >> 1) and ((v & 0x1) != (u & 0x1)):
                W += 1

            if u == v:
                Z += 1

            # if lsb(v) = 0 & u < v OR lsb(v) = 1 & u > v
            if (v == (v >> 1) << 1) and (u < v) or (v != (v >> 1) << 1) and (u > v):
                X += 1

            # vice versa
            if (v == (v >> 1) << 1) and (u > v) or (v != (v >> 1) << 1) and (u < v):
                Y += 1
            
            P += 1 
    
    a = 0.5 * (W + Z)
    b = 2 * X - P
    c = Y - X

    if a == 0:
        x = c / b
    
    discriminant = b ** 2 - (4 * a * c)
    if discriminant >= 0:
        rootpos = ((-1 * b) + sqrt(discriminant)) / (2 * a)
        rootneg = ((-1 * b) - sqrt(discriminant)) / (2 * a)

        if abs(rootpos) <= abs(rootneg):
            x = rootpos
        else:
            x = rootneg
    else:
        x = c / b

    if x == 0:
        x = c / b

    return x
    
if __name__ == "__main__":
    img = Image.open("pure.png")
    print(spa_test(img))
