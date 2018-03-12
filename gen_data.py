from PIL import Image, ImageDraw
from stegano import lsb
from string import ascii_letters
import os
import sys
import random
import shutil

TOOLS = ["Stegano"]

AMOUNT = 10

TEXT = "SUPERSECRET"

SEED = [i for i in range(10, 210, 10)]


def get_random_word(length):  # instead of os.urandom(5)
    return ''.join(random.choice(ascii_letters) for i in range(length))


def prepare():
    path = os.getcwd() + "/Tests"
    try:
        os.mkdir(path=path)
    except FileExistsError:
        pass
    os.chdir(path)


def hide_n_check(img, msg, tool, seed):
    decrypt = ""
    path = "pure.png"
    out_path = str(seed) + ".png"

    if tool == "Stegano":
        sec = lsb.hide(path, msg)
        sec.save(out_path)
        decrypt = lsb.reveal(out_path)

    if decrypt != msg:
        raise Exception("Ошибка извлечения")


def gen_images():
    for tool in TOOLS:
        try:
            os.mkdir(tool)
        except FileExistsError:
            pass
        os.chdir(tool)
        color = (0, 0, 120)
        img = Image.new('RGB', (90, 90), color)
        img_drawer = ImageDraw.Draw(img)

        img_drawer.text((10, 10), TEXT)
        img_drawer.text((20, 60), TEXT)
        img.save("pure.png")

        for s in SEED:
            random.seed(s)

            msg = get_random_word(s * 10)

            hide_n_check("pure.png", msg, tool, s)

        os.chdir("..")


def clear():
    os.chdir("..")
    shutil.rmtree("Tests")


if __name__ == "__main__":
    prepare()
    gen_images()
    #clear()
