import sys
import math
import numpy as np
from scipy.ndimage import imread
from scipy.optimize import minimize


class Rectangle(object):
    def __init__(self, x, y, w, h, color):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.color = color
    def __repr__(self):
        return "Rectangle({x}, {y}, {w}, {h}, <color>)".format(
            x=self.x, y=self.y, w=self.w, h=self.h)

def render_rectangle(rectangle: Rectangle, target: np.array):
    r, g, b = rectangle.color
    outside = 0
    for y in range(int(rectangle.y), math.ceil(rectangle.y + rectangle.h)):
        for x in range(int(rectangle.x), math.ceil(rectangle.x + rectangle.w)):
            xa = rectangle.x - x
            xa = xa if xa > 0 else 1

            if x >= int(rectangle.x + rectangle.w):
                xa = (rectangle.x + rectangle.w) - x

            if x >= 0 and x < target.shape[0]:
                target[x, y, 0] = r * xa
                target[x, y, 1] = g * xa
                target[x, y, 2] = b * xa
            else:
                outside += 1
    return outside

def render(shapes, target: np.array):
    for shape in shapes:
        render_rectangle(shape, target)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class Problem(object):
    def __init__(self, image: np.array) -> None:
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
        tmp = np.zeros(self.image.shape)
        render(self.unpack(x), tmp)
        e = np.divide(self.image, 255.0) - np.divide(tmp.data, 255.0)
        #print(np.linalg.norm(e))
        return np.linalg.norm(e)


def main():
    img = imread(sys.stdin.buffer)
    print(img.shape)
    problem = Problem(img)
    gray = (0x80, 0x80, 0x80)
    r0 = [Rectangle(2, 2, 28, 28, gray)]
    x0 = list(problem.pack(r0))
    res = minimize(problem.error, x0, method='CG',
        options=dict(disp=True))
    print(res)

if __name__ == "__main__":
    main()
