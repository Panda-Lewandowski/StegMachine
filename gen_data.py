from PIL import Image, ImageDraw
from stegano import lsb
from string import ascii_letters
import os
import random
import shutil
import logging
import hashlib

class Generator:
    def __init__(self, tools=None, text="SUPERSECRET", seed=[i for i in range(10, 210, 10)], log_lvl=logging.INFO):
        if tools is None:
            tools = ["Stegano"]
        self.tools = tools
        self.text = text
        self.seed = seed
        logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=log_lvl)
        logging.info('Generator was created.')

    def get_random_word(self, length):   # instead of os.urandom(5)
        return ''.join(random.choice(ascii_letters) for i in range(length))

    def prepare(self, ):
        path = os.getcwd() + "/Tests"
        try:
            os.mkdir(path=path)
            logging.info('Creating "Tests"...')
        except FileExistsError:
            logging.warning('Folder "Tests" was created before. Its contents will be cleared!')
            shutil.rmtree(path)
            os.mkdir(path=path)
        os.chdir(path)
        logging.info('Now here:' + os.getcwd())

    def hide_n_check(self, path, msg, tool, seed, pure_hash):
        decrypt = ""
        out_path = str(seed) + ".png"

        if tool == "Stegano":
            sec = lsb.hide(path, msg)
            sec.save(out_path)
            decrypt = lsb.reveal(out_path)

        if decrypt != msg:
            logging.error("Extraction error with " + out_path)
            raise Exception("Extraction error!")

        with open(out_path, 'rb') as hiden:
            data = hiden.read()
            md5_hash = hashlib.md5(data).hexdigest()

            if md5_hash == pure_hash:
                logging.error("MD5 hash error with " + out_path + ". Hashes match")
                raise Exception("MD5 hash error!")
        logging.info("Checking " + out_path + "... OK!")

    def gen_images(self):
        color = (0, 0, 120)
        img = Image.new('RGB', (90, 90), color)
        img_drawer = ImageDraw.Draw(img)

        img_drawer.text((10, 10), self.text)
        img_drawer.text((20, 60), self.text)
        img.save("pure.png")

        with open("pure.png", 'rb') as pure:
            data = pure.read()
            md5_hash = hashlib.md5(data).hexdigest()

        for tool in self.tools:
            try:
                os.mkdir(tool)
            except FileExistsError:
                logging.warning("Folder '"+ tool + "' was already exist.")
            os.chdir(tool)
            logging.info("Working with " + tool.upper() + "...")
            
            for s in self.seed:
                random.seed(s)
                msg = self.get_random_word(s * 10)
                self.hide_n_check("../pure.png", msg, tool, s, md5_hash)
                logging.info(tool.upper() + ": Hinding secret random text with seed " + str(s) + "...")
            os.chdir("..")

    def clear(self):
        logging.info("Clearing  all test files...")
        os.chdir("..")
        shutil.rmtree("Tests")


if __name__ == "__main__":
    gen = Generator()
    gen.prepare()
    gen.gen_images()
    gen.clear()
