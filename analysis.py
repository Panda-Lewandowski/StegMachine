from gen_data import Generator
from PIL import Image
from PIL.ExifTags import TAGS
import os
from math import sqrt
from scipy import stats, mean
import matplotlib.pyplot as plt
import logging
from methods.chi_square import chi_squared_test


class Analyzer:
    def __init__(self, generator=Generator()):
        self.generator = generator
        logging.info('Analyzer was created.')

    def exif(self, img):
        try:
            exif = { TAGS[k]: v for k, v in img._getexif().items() if k in TAGS }
            return exif
        except AttributeError:
            return {}

    def attack_chi_squared(self, mode="single"):
        fig, axs = plt.subplots(1, 4, tight_layout=True)

        list_of_chuncks = []
        os.chdir("Tests/")
        if mode == "single":
            os.chdir("SingleColor/")
        if mode == "random":
            os.chdir("RandomColor/") 
        if mode == "real":
            os.chdir("RealColor/")

        img = Image.open("pure.png")
        logging.info('Calculating chi_squared for '+ img.filename +' ...')
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
    # an.generator.prepare()
    # an.generator.gen_images()
    an.attack_chi_squared(mode="real")
    # an.generator.clear()

