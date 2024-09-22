import sys
from . import replaceSOH

def main():
    if len(sys.argv) < 3:
        print("Usage: kitetsu <log filename> <output filename>")
        sys.exit(1)

    input_log = sys.argv[1]
    output_file = sys.argv[2]

    result = replaceSOH(input_log, output_file)
    if result == 0:
        print("Success replaced")
    else:
        print("Error replaced")
