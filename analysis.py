from gen_data import prepare, clear, TOOLS, SEED
from PIL import Image
import os


def calc_colors(img):
    width, height = img.size
    pix = img.load()
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            print(a, b, c)


def crop_4_chuncks(img, s):
    chunk1 = img.crop((0, 0, 50, 50))
    chunk2 = img.crop((50, 0, 100, 50))
    chunk3 = img.crop((0, 50, 50, 100))
    chunk4 = img.crop((50, 50, 100, 100))

    chunk1.save(str(s) + "chunk1.png")
    chunk2.save(str(s) + "chunk2.png")
    chunk3.save(str(s) + "chunk3.png")
    chunk4.save(str(s) + "chunk4.png")


def analyze():
    for tool in TOOLS:
        os.chdir(tool)
        for s in SEED:
            img = Image.open(str(s) + ".png")
            calc_colors(img)
            if s == 10:
                crop_4_chuncks(img, s)


if __name__ == "__main__":
    prepare()
    analyze()
