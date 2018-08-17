from PIL import Image
from PIL.ExifTags import TAGS
import os
import logging
from methods.chi_square import chi_squared_test
from methods.sample_pairs import spa_test
from methods.RS import rs_test
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

    def visual_attack(self, img, join=False, bitnum=1):
        logging.info('Visualising lsb for '+ img.filename +' ...🌀')
        height, width = img.size

        if join == False:
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
                # os.system("open " + name)
                img_ch.show()
        else:
            img_ch = Image.new("RGB", (height, width), color=(0, 0, 0))
            for i in range(height):
                for j in range(width):
                    pixel = img.getpixel((i, j))
                    if len(pixel) == 4:
                        pixel = pixel[:-1]
                    new_pixel = [0, 0, 0]
                    for k in range(3):
                        if int(bin(pixel[k])[-1]) == 1:
                            new_pixel[k] = 255
                        else:
                            new_pixel[k] = 0

                    img_ch.putpixel((i, j), tuple(new_pixel))
            img_ch.save("LSB-" + img.filename.split(".")[0] + ".bmp")
            logging.info("Openning LSB image...🌀")
            # os.system("open " + name)
            img_ch.show()



    def chi_squared_attack(self, img):
        logging.info('Calculating chi_squared for '+ img.filename +' ...🌀')
        eps = 1e-5
        channels = img.split()
        height, width = img.size

        img_to_blend = Image.new("RGB", (height, width), color=(0, 0, 0))
    
        for i in range(height):
            prob = 0
            for ch in channels:
                data = ch.crop((0, i, width, i+1))
                prob += chi_squared_test(data)[1]
            prob /= 3
            if 0.5 - eps < prob < 0.5 + eps:
                for j in range(width):
                    img_to_blend.putpixel((j, i), (209, 167, 27))
            elif prob < 0.5 - eps:
                for j in range(width):
                    img_to_blend.putpixel((j, i), (112, 209, 27))
            elif prob > 0.5 + eps:
                for j in range(width):
                    img_to_blend.putpixel((j, i), (255, 0, 0))

        result = Image.blend(img, img_to_blend, 0.5)
        result.save("chi-" + img.filename)
        result.show()

    def spa_attack(self, img):
        logging.info("Calculating spa beta for " + img.filename +' ...🌀')
        estimate = spa_test(img)
        logging.info("SPA estimate for "+ img.filename + " is " + str(estimate))

    def rs_attack(self, img):
        logging.info("Calculating rs estimate for " + img.filename +' ...🌀')
        logging.info("It will take a couple of minutes...")
        estimate = rs_test(img)
        logging.info("RS estimate for "+ img.filename + " is " + str(estimate))

if __name__ == "__main__":
    an = Analyzer()
    # an.check_tests()
    an.visual_attack(Image.open("30.png"))
    # an.attack_chi_squared(mode="real")
    # an.generator.clear()

