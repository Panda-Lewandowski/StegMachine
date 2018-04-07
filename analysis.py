from gen_data import prepare, clear, TOOLS, SEED
from PIL import Image
import os
from math import sqrt
from scipy.stats import chisquare


def chi_squared_test(img):
    k = img.size[0] * img.size[1]
    meas_freq_r = calc_colors(img, channel='r')
    meas_freq_g = calc_colors(img, channel='g')
    meas_freq_b = calc_colors(img, channel='b')

    theor_freq = {x: k/256 for x in range(256)}

    chi, pval = chisquare([meas_freq_r[x] for x in meas_freq_r.keys()],
                          [theor_freq[x] for x in theor_freq.keys()])
    print(chi, pval)


def calc_colors(img, channel='r'):
    width, height = img.size
    amount_dict = {x: 0 for x in range(256)}
    if channel == 'r':
        ch = img.split()[0]
    elif channel == 'g':
        ch = img.split()[1]
    elif channel == 'b':
        ch = img.split()[2]
    pix = ch.load()
    for i in range(width):
        for j in range(height):
            amount_dict[pix[i, j]] += 1

    amount_dict = {key: amount_dict[key]/(width*height) for key in amount_dict.keys()}
    return amount_dict


def crop_n_chunks(img, n):
    x = y = int(sqrt(n))
    piece_x = int(img.size[0] // x)
    piece_y = int(img.size[1] // y)
    start_x = 0
    start_y = 0
    count = 1

    for i in range(y):
        for j in range(x):
            chnk = img.crop((start_x, start_y, start_x + piece_x, start_y + piece_y))
            chnk.save("chunk" + str(count) + ".png")
            start_x += piece_x
            count += 1
        start_y += piece_y
        start_x = 0


def del_n_chunks(n):
    for i in range(n):
        os.remove("chunk" + str(i + 1) + ".png")


def analyze():
    for tool in TOOLS:
        os.chdir(tool)
        for s in SEED:
            img = Image.open(str(s) + ".png")
            crop_n_chunks(img, 9)
            for i in range(1, 10):
                chnk = Image.open("chunk" + str(i) + ".png")
                print("\n\n_______chunk" + str(i) + ".png_________")
                chi_squared_test(chnk)
            del_n_chunks(9)
        os.chdir("..")


if __name__ == "__main__":
    prepare()
    analyze()

