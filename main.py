import sys
from netpbm import imread, Image


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
    for y in range(rectangle.y, rectangle.y + rectangle.h):
        for x in range(rectangle.x, rectangle.x + rectangle.w):
            r, g, b = rectangle.color
            o = target.stride * y + x
            data[o + 0] = r
            data[o + 1] = g
            data[o + 2] = b


def render(shapes, target: Image):
    for shape in shapes:
        render_rectangle(shape, target)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


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


    def error(self, y):
        """Returns error vector"""
        tmp = Image(self.image.width, self.image.height)
        render(y, tmp)
        return 0


def main():
    img = imread(sys.stdin.buffer)

    white = (0xff, 0xff, 0xff)
    r0 = [Rectangle(0, 0, img.width, img.height, white)]
    problem = Problem(img)
    x = list(problem.pack(r0))
    y = list(problem.unpack(x))
    print(r0)
    print(y)
    print(problem.error(r0))


main()
