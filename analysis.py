from gen_data import Generator
from PIL import Image
from PIL.ExifTags import TAGS
import os
import logging
from methods.chi_square import chi_squared_test
import numpy as np


class Analyzer:
    def __init__(self, log_lvl=logging.INFO):
        logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=log_lvl)
        logging.info('Analyzer was created.')

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
            return {}

    def visual_attack(self, img):
        logging.info('Visualising lsb for '+ img.filename +' ...🌀')
        height, width = img.size

        r, g, b = img.split()

        channel = r.load()
        img_r = Image.new("RGB", (height, width), color=(0, 0, 0))

        for i in range(height):
            for j in range(width):
                bit = int((bin(channel[i, j]))[-1])
                if bit == 1:
                    img_r.putpixel((i, j), 255)

        img_r.save("red-" + img.filename.split(".")[0] + ".bmp")

        channel = g.load()
        img_g = Image.new("RGB", (height, width), color=(0, 255, 0))

        for i in range(height):
            for j in range(width):
                bit = int((bin(channel[i, j]))[-1])
                if bit == 1:
                    img_g.putpixel((i, j), 0)

        img_g.save("green-" + img.filename.split(".")[0] + ".bmp")

        channel = b.load()
        img_b = Image.new("RGB", (height, width), color=(0, 0, 255))

        for i in range(height):
            for j in range(width):
                bit = int((bin(channel[i, j]))[-1])
                if bit == 1:
                    img_b.putpixel((i, j), 0)

        img_b.save("blue-" + img.filename.split(".")[0] + ".bmp")                

    def attack_chi_squared(self, img):
        logging.info('Calculating chi_squared for '+ img.filename +' ...🌀')
        # for i in range(1, self.n_chunks + 1):
        #     chnk = Image.open("chunk" + str(i) + ".png")
        #     list_of_chuncks.append(mean(chi_squared_test(chnk)[0]))

        # Analyzer.del_n_chunks(self.n_chunks)
        # axs[0].bar([i+1 for i in range(self.n_chunks)], height=list_of_chuncks)
        # axs[0].set_title("Pure image")
        # axs[0].set_ylabel("Chi Squared")

        # for tool in self.generator.tools:
        #     os.chdir(tool)
        #     for s in self.generator.seed:
        #         list_of_chuncks = []
        #         img = Image.open(str(s) + ".png")
        #         logging.info(tool.upper() + ': Calculating chi_squared for '+ img.filename +' ...')
        #         Analyzer.crop_n_chunks(img, self.n_chunks)
        #         for i in range(1, self.n_chunks + 1):
        #             chnk = Image.open("chunk" + str(i) + ".png")
        #             list_of_chuncks.append(mean(chi_squared_test(chnk)[0]))
        #         if s == 10:
        #             axs[1].set_title('Seed 10')
        #             axs[1].bar([i + 1 for i in range(self.n_chunks)], height=list_of_chuncks)
        #         if s == 100:
        #             axs[2].set_title('Seed 100')
        #             axs[2].bar([i + 1 for i in range(self.n_chunks)], height=list_of_chuncks)
        #         if s == 200:
        #             axs[3].set_title('Seed 200')
        #             axs[3].bar([i + 1 for i in range(self.n_chunks)], height=list_of_chuncks)

        #         Analyzer.del_n_chunks(self.n_chunks)
        #     os.chdir("..")
        #     plt.show()


if __name__ == "__main__":
    an = Analyzer()
    # an.check_tests()
    an.visual_attack(Image.open("70.png"))
    an.visual_attack(Image.open("pure.png"))
    # an.attack_chi_squared(mode="real")
    # an.generator.clear()

