import sys
from argparse import ArgumentParser,Namespace

def parse_args() -> Namespace:

    parser = ArgumentParser(
                    prog='cam-cli',
                    description='cambridge command utils for you.'
            )
    # word
    parser.add_argument('word')

    # optional.
    parser.add_argument('-c','--chinese',help="translate to chinese.",action="store_true")

    # default param.
    if len(sys.argv) == 1:
        sys.argv.append("--help")

    return parser.parse_args()