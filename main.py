import sys
from netpbm import imread, Image
import math
import numpy as np
from scipy.optimize import minimize

class Rectangle(object):
    def __init__(self, x, y, w, h, color):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.color = color
    def __repr__(self):
        return "Rectangle({x}, {y}, {w}, {h}, <color>)".format(
            x=self.x, y=self.y, w=self.w, h=self.h)

def render_rectangle(rectangle: Rectangle, target: Image):
    data = target.data
    r, g, b = rectangle.color
    for y in range(int(rectangle.y), math.ceil(rectangle.y + rectangle.h)):
        for x in range(int(rectangle.x), math.ceil(rectangle.x + rectangle.w)):
            xa = rectangle.x - x
            xa = xa if xa > 0 else 1

            if x >= int(rectangle.x + rectangle.w):
                xa = (rectangle.x + rectangle.w) - x

            o = target.stride * y + x * 3
            if o >= 0 and o < len(data):
                data[o + 0] = int(r) * xa
                data[o + 1] = int(g) * xa
                data[o + 2] = int(b) * xa


def render(shapes, target: Image):
    for shape in shapes:
        render_rectangle(shape, target)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def everything(image: Image) -> np.array:
    """returns all color data as numpy array"""
    return np.frombuffer(image, dtype=np.dtype('b'))


class Problem(object):
    def __init__(self, image: Image) -> None:
        self.image = image

    def pack(self, y):
        for r in y:
            yield r.x
            yield r.y
            yield r.w
            yield r.h
            yield r.color[0]
            yield r.color[1]
            yield r.color[2]

    def unpack(self, x):
        for x, y, w, h, r, g, b in chunks(x, 7):
            color = (r, g, b)
            yield Rectangle(x, y, w, h, color)


    def error(self, x):
        """Returns error vector"""
        #print(x)
        tmp = Image(self.image.width, self.image.height)
        render(self.unpack(x), tmp)
        e = (everything(self.image.data)/255.0) - (np.array(tmp.data) / 255.0)
        print(np.linalg.norm(e))
        return np.linalg.norm(e)


def main():
    img = imread(sys.stdin.buffer)

    problem = Problem(img)
    white = (0xff, 0xff, 0xff)
    gray = (0x80, 0x80, 0x80)
    r0 = [Rectangle(2, 2, img.width-4, img.height-4, gray)]
    x0 = list(problem.pack(r0))
    res = minimize(problem.error, x0, method='CG',
        options=dict(disp=True))
    print(res)

if __name__ == "__main__":
    main()
