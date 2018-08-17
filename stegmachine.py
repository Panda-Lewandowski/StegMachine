import sys
import logging
from modules.analysis import Analyzer
from PIL import Image

def usage(prog_name):
    print("""
    StegMachine is a flexible tool for stegoanalysis.
    Usage:
        {0} exif <path to image file>
        {0} visual <path to image file> 
        {0} visual -b <n> <path to image file>
        {0} chi <path to image file>
        {0} spa <path to image file>
        {0} rs <path to image file>
        {0} generate 
        {0} help
    """.format(prog_name))
    sys.exit()

def help(prog_name):
    print("""
    USAGE: python3 {0} <module> <params> 
    ______________________________________\n
    MODULES
    \t🔹exif <path to image file>               exif extracting module\n
    \t🔹visual <params> <path to image file>    module for visual attack
    \t       -b <n>        the number of lsb in which the message is embed  \n
    \t🔹chi <path to image file>                module for chi-squared attack \n
    \t🔹spa <path to image file>                module for sample pair attack \n
    \t🔹rs <path to image file>                 module for rs-method attack \n
    \t🔹generate                                genenrate data set with specified tools\n
    \t🔹help                                    hint output\n
    """.format(prog_name))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage(sys.argv[0])
   
    if len(sys.argv) == 2 and sys.argv[1] == "help":
        help(sys.argv[0]) 
    else: 
        an = Analyzer()
        if sys.argv[1] == "exif":
            an.exif(Image.open(sys.argv[2]))
        elif sys.argv[1] == "visual":
            if sys.argv[2] == "-b":
                an.visual_attack(Image.open(sys.argv[2]), bitnum=sys.argv[3])
            elif sys.argv[2] == "-j":
                an.visual_attack(Image.open(sys.argv[3]), join=True)
            else:
                an.visual_attack(Image.open(sys.argv[2]))
        elif sys.argv[1] == "chi":
            an.chi_squared_attack(Image.open(sys.argv[2]))
        elif sys.argv[1] == "spa":
            an.spa_attack(Image.open(sys.argv[2]))
        elif sys.argv[1] == "rs":
            an.rs_attack(Image.open(sys.argv[2]))
        else:
            usage(sys.argv[0])
            logging.info("Invalid operation specified! ❌")