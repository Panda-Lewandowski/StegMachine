from PIL import Image, ImageDraw
from stegano import lsb
import os
import sys
import shutil
import random, string

TOOLS = ["Stegano"]

AMOUNT = 10

MSG = "SECRET"

DENSITY = [i for i in range(10, 60, 10)]


def prepare():
    path = os.getcwd() + "/Tests"
    os.mkdir(path=path)
    os.chdir(path)


def gen_images():
    for tool in TOOLS:
        os.mkdir(tool)
        os.chdir(tool)
        color = (0, 0, 120)

        for d in DENSITY:
            img = Image.new('RGB', (100, 100), color)
            img_drawer = ImageDraw.Draw(img)

            img_drawer.text((10, 10), MSG)
            img.save(str(d) + "%.png")
            # lsb.hide(str(d) + "%.png", "Hello World")
            # print(lsb.reveal(str(d) + "%.png"))

        os.chdir("..")


def clear():
    os.chdir("..")
    shutil.rmtree("Tests")


if __name__ == "__main__":
    prepare()
    gen_images()
    clear()
