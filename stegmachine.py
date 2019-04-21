import argparse
import logging
import sys

from PIL import Image

from modules.analysis import Analyzer
from tests import start_tests

parser = argparse.ArgumentParser(add_help=True, 
                                 description='StegMachine is a flexible tool for stegoanalysis.')

mode_group = parser.add_mutually_exclusive_group(required=True)
mode_group.add_argument('--analysis', nargs='?', type=str, choices=['exif', 'chi', 'spa', 'rs', 'visual'], 
                        help='Analyzing  module')
mode_group.add_argument('--hiding', nargs='?', type=str, choices=[], help='Hiding  module')
mode_group.add_argument('--test', action='store_true',  help='Test  module')
mode_group.add_argument('--generation', action='store_true', help='Generation  module')

params_group = parser.add_mutually_exclusive_group(

)
params_group.add_argument('-b', nargs='?',  type=int, choices=range(0, 255), metavar='from 0 to 255', 
                        help="What bit should be displayed in the visual attack")
params_group.add_argument('-j',action='store_true',
                        help="Joins channels into one image")

parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument('ouput_dir', type=str)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        parser.print_help()
    else:
        args = parser.parse_args()
        img = Image.open(args.input_file.name)
        # img.verify()

        if args.analysis:
            an = Analyzer()
            
            if args.analysis == "exif":
                an.exif(args.input_file.name)
            elif args.analysis == "visual":
                if args.b:
                    an.visual_attack(img, bitnum=args.b)
                elif args.j:
                    print(args.j)
                    an.visual_attack(img, join=True)
                else:
                    an.visual_attack(img)
            elif args.analysis == "chi":
                an.chi_squared_attack(img)
            elif  args.analysis == "spa":
                an.spa_attack(img)
            elif args.analysis == "rs":
                an.rs_attack(img)
        elif args.test:
            start_tests()
        else:
            logging.info("Invalid operation specified! ❌")
