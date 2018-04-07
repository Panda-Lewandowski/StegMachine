from gen_data import prepare, clear, TOOLS, SEED
from PIL import Image
import os
from math import gamma, e, sqrt
import matplotlib.pyplot as plt
import scipy.integrate as integrate


def chi_squared_test(img):
    k = img.size[0] * img.size[1]
    meas_freq = calc_colors(img)
    theor_freq = {}
    for key in meas_freq.keys():
        n = 0
        if tuple([key[0] + 1, key[1], key[2]]) in meas_freq.keys():
            n += meas_freq[tuple([key[0] + 1, key[1], key[2]])]

        if tuple([key[0], key[1] + 1, key[2]]) in meas_freq.keys():
            n += meas_freq[tuple([key[0], key[1] + 1, key[2]])]

        if tuple([key[0], key[1], key[2] + 1]) in meas_freq.keys():
            n += meas_freq[tuple([key[0], key[1], key[2] + 1])]

        theor_freq.update({key: meas_freq[key] + n / 4})

    # for i in meas_freq:
    #     meas_freq[i] /= k
    #     theor_freq[i] /= k

    v = len(meas_freq)
    chi_sq = sum((meas_freq[i] - theor_freq[i])**2 / theor_freq[i] for i in meas_freq)
    print(integrate.quad(lambda x: integrand(x, v), 0, chi_sq))
    prob = 1 - (1 / (2 ** (v / 2) * gamma(v / 2))) * integrate.quad(lambda x: integrand(x, v), 0, chi_sq)[0]
    return chi_sq


def integrand(x, k):
    return (e ** (-x / 2)) * (x ** (k / 2 - 1))


def calc_colors(img):
    width, height = img.size
    amount_dict = {}
    pix = img.load()
    for i in range(width):
        for j in range(height):
            if pix[i, j] not in amount_dict.keys():
                amount_dict.update({pix[i, j]: 1})
            else:
                amount_dict[pix[i, j]] += 1
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
                chi_squared_test(chnk)
            del_n_chunks(9)
        os.chdir("..")


if __name__ == "__main__":
    prepare()
    analyze()

