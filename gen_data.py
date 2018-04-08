from PIL import Image, ImageDraw
from stegano import lsb
from string import ascii_letters
import os
import random
import shutil


class Generator:
    def __init__(self, tools=None, text="SUPERSECRET", seed=[i for i in range(10, 210, 10)]):
        if tools is None:
            tools = ["Stegano"]
        self.tools = tools
        self.text = text
        self.seed = seed

    def get_random_word(self, length):   # instead of os.urandom(5)
        return ''.join(random.choice(ascii_letters) for i in range(length))

    def prepare(self, ):
        path = os.getcwd() + "/Tests"
        try:
            os.mkdir(path=path)
        except FileExistsError:
            pass
        os.chdir(path)

    def hide_n_check(self, path, msg, tool, seed):
        decrypt = ""
        out_path = str(seed) + ".png"

        if tool == "Stegano":
            sec = lsb.hide(path, msg)
            sec.save(out_path)
            decrypt = lsb.reveal(out_path)

        if decrypt != msg:
            raise Exception("Ошибка извлечения")

    def gen_images(self):
        for tool in self.tools:
            try:
                os.mkdir(tool)
            except FileExistsError:
                pass
            os.chdir(tool)
            color = (0, 0, 120)
            img = Image.new('RGB', (90, 90), color)
            img_drawer = ImageDraw.Draw(img)

            img_drawer.text((10, 10), self.text)
            img_drawer.text((20, 60), self.text)
            img.save("pure.png")

            for s in self.seed:
                random.seed(s)

                msg = self.get_random_word(s * 10)

                self.hide_n_check("pure.png", msg, tool, s)

            os.chdir("..")

    def clear(self):
        os.chdir("..")
        shutil.rmtree("Tests")


if __name__ == "__main__":
    gen = Generator()
    gen.prepare()
    gen.gen_images()

