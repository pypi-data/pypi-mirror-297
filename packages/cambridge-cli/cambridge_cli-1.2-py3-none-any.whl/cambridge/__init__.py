from .dictionary import Dictionary
from .args import parse_args

def main():
    args = parse_args()
    d = Dictionary(args.word)
    d.print()