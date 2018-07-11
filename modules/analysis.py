from PIL import Image
from PIL.ExifTags import TAGS
import os
import logging
from methods.chi_square import chi_squared_test
import numpy as np


class Analyzer:
    def __init__(self, log_lvl=logging.INFO):
        logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=log_lvl)
        # logging.info('Analyzer was created.')

    def check_tests(self):
        try:
            os.chdir("Tests/")
        except FileNotFoundError:
            logging.error("Please, generate test sample or rename it to 'Tests'!❗️")
        else:
            os.chdir('..')
            logging.info("Everything is fine with the test folder.✅")

    def exif(self, img):
        try:
            exif = { TAGS[k]: v for k, v in img._getexif().items() if k in TAGS }
            return exif
        except AttributeError:
            logging.info("Sorry, there is no exif data!")

    def visual_attack(self, img, bitnum=1):
        logging.info('Visualising lsb for '+ img.filename +' ...🌀')
        height, width = img.size

        channels = img.split()

        colors = [(0, 0, 0), (0, 255, 0), (0, 0, 255)]
        suffixes = ['red', 'green', 'blue']

        for k in range(3):
            channel = channels[k].load()
            img_ch = Image.new("RGB", (height, width), color=colors[k])

            for i in range(height):
                for j in range(width):
                    bit = int((bin(channel[i, j]))[-bitnum])
                    if bit == 1:
                        if k == 0:
                            img_ch.putpixel((i, j), 255)
                        else:
                            img_ch.putpixel((i, j), 0)
            name = suffixes[k] + "-" + img.filename.split(".")[0] + ".bmp"
            img_ch.save(name)
            logging.info("Openning " + suffixes[k] + " component...🌀")
            os.system("open " + name)

    def chi_squared_attack(self, img):
        logging.info('Calculating chi_squared for '+ img.filename +' ...🌀')

    def spa_attack(self, img):
        logging.info("Calculating spa beta for " + img.filename +' ...🌀')


if __name__ == "__main__":
    an = Analyzer()
    # an.check_tests()
    an.visual_attack(Image.open("30.png"))
    # an.attack_chi_squared(mode="real")
    # an.generator.clear()

