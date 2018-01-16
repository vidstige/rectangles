import sys
from netpbm import imread, Image


class Problem(object):
    def __init__(self, image: Image) -> None:
        pass

    def error(self, x):
        return 0


def main():
    img = imread(sys.stdin.buffer)
    problem = Problem(img)
    print(problem.error(0))


main()
