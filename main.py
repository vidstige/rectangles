import sys
from netpbm import imread

def main():
    imread(sys.stdin.buffer)

main()
