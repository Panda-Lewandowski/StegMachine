from PIL import Image, ImageDraw
from stegano import lsb
from string import ascii_letters
import os
import sys
import random
import shutil
import logging
import hashlib
import cv2        
import numpy
from LSBSteganography.LSBSteg import LSBSteg
#from cloackedpixel.lsb import embed, extract
from settings import full_spectrum_tools


class Generator:
    def __init__(self, tools=None, text="SUPERSECRET", seed=[i for i in range(10, 110, 10)], log_lvl=logging.INFO):
        if tools is None:
            tools = full_spectrum_tools
        self.tools = tools
        self.text = text
        self.seed = seed
        logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=log_lvl)
        logging.info('Generator was created.')

    def get_random_word(self, length):
        return ''.join(random.choice(ascii_letters) for i in range(length))

    def prepare(self, ):
        path = os.getcwd() + "/Tests"
        try:
            os.mkdir(path=path)
            logging.info('Creating "Tests"...')
        except FileExistsError:
            logging.warning('Folder "Tests" was created before. Its contents will be cleared!❗️')
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
            
        if tool == "OpenStego":
            with open('msg.txt', 'w') as payload:
                payload.write(msg)

            ret_code = os.system("java -jar ../../../openstego.jar embed -mf msg.txt -sf " + out_path)

            if ret_code == 0:
                ret_code = os.system("java -jar ../../../openstego.jar extract -sf " + out_path + " -xd . > /dev/null")
                if ret_code == 0:
                    with open("msg.txt") as decrypt_file:
                        decrypt = decrypt_file.read()
                        
            os.remove('msg.txt')

        if tool == "cloacked-pixel":
            with open('msg.txt', 'w') as payload:
                payload.write(msg)

            ret_code = os.system("python ../../../cloackedpixel/lsb.py hide ../pure.png msg.txt qwerty")    #> /dev/null")
            if ret_code == 0:
                os.chdir("..")
                os.rename("pure.png-stego.png", out_path) 
                shutil.move(out_path, "cloacked-pixel/")
                os.chdir("cloacked-pixel/")
                ret_code = os.system("python ../../../cloackedpixel/lsb.py extract " + os.path.abspath(out_path) + " out.txt qwerty") #> /dev/null")
                if ret_code == 0:
                    with open("out.txt") as decrypt_file:
                        decrypt = decrypt_file.read()
                else:
                    raise Exception("Extacting error!❌")
            else:
                raise Exception("Hiding error!❌")

            os.remove('msg.txt')
            os.remove('out.txt')

        if tool == "LSBSteg":
            steg = LSBSteg(cv2.imread("../pure.png"))
            img_encoded = steg.encode_text(msg)
            cv2.imwrite(out_path, img_encoded)

            im = cv2.imread(out_path)
            steg = LSBSteg(im)
            decrypt = steg.decode_text()

        if decrypt != msg:
            logging.error("Extraction error with " + out_path)
            raise Exception("Extraction error!❌")

        with open(out_path, 'rb') as hiden:
            data = hiden.read()
            md5_hash = hashlib.md5(data).hexdigest()

            if md5_hash == pure_hash:
                logging.error("MD5 hash error with " + out_path + ". Hashes match")
                raise Exception("MD5 hash error!❌")
        logging.info("Checking " + out_path + "... OK!✅")

    def generate_images(self, height, width, mode="single"):
        if mode == "single":
            logging.info("Generate single color imeges...🌀")
            os.mkdir(path="SingleColor/")
            os.chdir("SingleColor")
            random.seed()
            color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            img = Image.new('RGB', (height, width), color)

        if mode == "random":
            logging.info("Generate random color imeges...🌀")
            os.mkdir(path="RandomColor/")
            os.chdir("RandomColor")
            a = numpy.random.rand(height, width,3) * 255
            img = Image.fromarray(a.astype('uint8')).convert('RGBA')

        if mode == "real":
            logging.info("Generate real imeges...🌀")
            img = Image.open("../test.png")
            os.mkdir(path="RealColor/")
            os.chdir("RealColor")

        img_drawer = ImageDraw.Draw(img)
        img.save("pure.png")

        with open("pure.png", 'rb') as pure:
            data = pure.read()
            md5_hash = hashlib.md5(data).hexdigest()

        for tool in self.tools:
            try:
                os.mkdir(tool)
            except FileExistsError:
                logging.warning("Folder '"+ tool + "' was already exist.❗️")
            os.chdir(tool)
            logging.info("Working with " + tool.upper() + "...")
            
            for s in self.seed:
                random.seed(s)
                msg = self.get_random_word(s * height * width // 275)
                self.hide_n_check("../pure.png", msg, tool, s, md5_hash)
                logging.info(tool.upper() + ": Hinding secret random text with seed " + str(s) + "...")
            os.chdir("..")
        os.chdir("..")

    def clear(self):
        logging.info("Clearing  all test files...🌀")
        os.chdir("..")
        shutil.rmtree("Tests")


if __name__ == "__main__":
    gen = Generator()
    # gen.prepare()
    gen.generate_images(900, 900)
    gen.generate_images(900, 900, mode="random")
    gen.generate_images(900, 900, mode="real")
    #   gen.clear()
