from gen_data import prepare, clear, TOOLS, SEED
from PIL import Image
import os
from math import gamma, e
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

    v = len(meas_freq) - 1
    chi_sq = sum((meas_freq[i] - theor_freq[i])**2 / theor_freq[i] for i in meas_freq)
    # prob = 1 - (1 / (2 ** (v / 2) * gamma(v / 2))) * integrate.quad(lambda x: integrand(x, v), 0, chi_sq)[0]
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


def crop_4_chuncks(img):
    chunk1 = img.crop((0, 0, 50, 50))
    chunk2 = img.crop((50, 0, 100, 50))
    chunk3 = img.crop((0, 50, 50, 100))
    chunk4 = img.crop((50, 50, 100, 100))

    chunk1.save("chunk1.png")
    chunk2.save("chunk2.png")
    chunk3.save("chunk3.png")
    chunk4.save("chunk4.png")


def crop_9_chunks(img):
    chunk1 = img.crop((0, 0, 30, 30))
    chunk2 = img.crop((30, 0, 60, 30))
    chunk3 = img.crop((60, 0, 90, 30))

    chunk4 = img.crop((0, 30, 30, 60))
    chunk5 = img.crop((30, 30, 60, 60))
    chunk6 = img.crop((60, 30, 90, 60))

    chunk7 = img.crop((0, 60, 30, 90))
    chunk8 = img.crop((30, 60, 60, 90))
    chunk9 = img.crop((60, 60, 90, 90))

    chunk1.save("chunk1.png")
    chunk2.save("chunk2.png")
    chunk3.save("chunk3.png")
    chunk4.save("chunk4.png")
    chunk5.save("chunk5.png")
    chunk6.save("chunk6.png")
    chunk7.save("chunk7.png")
    chunk8.save("chunk8.png")
    chunk9.save("chunk9.png")


def del_9_chunks():
    os.remove("chunk1.png")
    os.remove("chunk2.png")
    os.remove("chunk3.png")
    os.remove("chunk4.png")
    os.remove("chunk5.png")
    os.remove("chunk6.png")
    os.remove("chunk7.png")
    os.remove("chunk8.png")
    os.remove("chunk9.png")


def analyze():

    for tool in TOOLS:
        os.chdir(tool)
        for s in SEED:
            img = Image.open(str(s) + ".png")
            crop_9_chunks(img)
            for i in range(1, 10):
                chnk = Image.open("chunk" + str(i) + ".png")
                print(s, i, chi_squared_test(chnk))
            del_9_chunks()
        os.chdir("..")


if __name__ == "__main__":
    prepare()
    analyze()

