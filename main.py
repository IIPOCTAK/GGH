import argparse
from colored import fg, attr
from ggh import GGH


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("message", help="Message for encrypt and decrypt",
                        type=str)
    parser.add_argument("-v", "--verbose",
                        help="Make output more verbosity",
                        action="store_true", default=False)
    args = parser.parse_args()
    try:
        ggh_object = GGH(args.message, args.verbose)
        ggh_object.algorithm()
    except Exception as error:
        print(f"{fg(1)}Unexpected error is occured. Info: {error}{attr('reset')}")


if __name__ == "__main__":
    main()
