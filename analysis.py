from gen_data import Generator
from PIL import Image
import os
from math import sqrt
from scipy import stats, mean
import matplotlib.pyplot as plt


class Analyzer:
    def __init__(self, num=25, generator=Generator()):
        self.n_chunks = num
        self.generator = generator

    @staticmethod
    def chi_squared_test(img):
        meas_freq_r = Analyzer.calc_colors(img, channel='r')
        meas_freq_g = Analyzer.calc_colors(img, channel='g')
        meas_freq_b = Analyzer.calc_colors(img, channel='b')

        theor_freq = {x: 1/256 for x in range(256)}

        chis = [0, 0, 0]
        probs = [0, 0, 0]

        chis[0], probs[0] = stats.chisquare([meas_freq_r[x] for x in meas_freq_r.keys()],
                                            [theor_freq[x] for x in theor_freq.keys()])
        chis[1], probs[1] = stats.chisquare([meas_freq_g[x] for x in meas_freq_g.keys()],
                                            [theor_freq[x] for x in theor_freq.keys()])
        chis[2], probs[2] = stats.chisquare([meas_freq_b[x] for x in meas_freq_b.keys()],
                                            [theor_freq[x] for x in theor_freq.keys()])

        return chis, probs

    @staticmethod
    def calc_colors(img, channel='r'):
        width, height = img.size
        amount_dict = {x: 0 for x in range(256)}
        if channel == 'r':
            ch = img.split()[0]
        elif channel == 'g':
            ch = img.split()[1]
        elif channel == 'b':
            ch = img.split()[2]
        else:
            ch = None
        if ch:
            pix = ch.load()
            for i in range(width):
                for j in range(height):
                    amount_dict[pix[i, j]] += 1

            amount_dict = {key: amount_dict[key]/(width*height) for key in amount_dict.keys()}
        return amount_dict

    @staticmethod
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

    @staticmethod
    def del_n_chunks(n):
        for i in range(n):
            os.remove("chunk" + str(i + 1) + ".png")

    def analyzeLSB(self):
        for tool in self.generator.tools:
            os.chdir(tool)

            fig, axs = plt.subplots(1, 4, tight_layout=True)

            list_of_chuncks = []
            img = Image.open("pure.png")
            Analyzer.crop_n_chunks(img, self.n_chunks)
            for i in range(1, self.n_chunks + 1):
                chnk = Image.open("chunk" + str(i) + ".png")
                list_of_chuncks.append(mean(Analyzer.chi_squared_test(chnk)[0]))

            Analyzer.del_n_chunks(self.n_chunks)
            axs[0].bar([i+1 for i in range(self.n_chunks)], height=list_of_chuncks)
            axs[0].set_title("Pure image")
            axs[0].set_ylabel("Chi Squared")

            for s in self.generator.seed:
                list_of_chuncks = []
                img = Image.open(str(s) + ".png")
                Analyzer.crop_n_chunks(img, self.n_chunks)
                for i in range(1, self.n_chunks + 1):
                    chnk = Image.open("chunk" + str(i) + ".png")
                    list_of_chuncks.append(mean(Analyzer.chi_squared_test(chnk)[0]))
                if s == 10:
                    axs[1].set_title('Seed 10')
                    axs[1].bar([i + 1 for i in range(self.n_chunks)], height=list_of_chuncks)
                if s == 100:
                    axs[2].set_title('Seed 100')
                    axs[2].bar([i + 1 for i in range(self.n_chunks)], height=list_of_chuncks)
                if s == 200:
                    axs[3].set_title('Seed 200')
                    axs[3].bar([i + 1 for i in range(self.n_chunks)], height=list_of_chuncks)

                Analyzer.del_n_chunks(self.n_chunks)
            os.chdir("..")
            plt.show()


if __name__ == "__main__":
    an = Analyzer()
    an.generator.prepare()
    an.analyzeLSB()

