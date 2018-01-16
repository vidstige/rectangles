class Image(object):
    def __init__(self, width, height, data=None):
        self.width = width
        self.height = height
        self.stride = width * 3
        self.data = data or bytearray([0] * self.stride * self.height)


class NetPBMException(Exception):
    pass


def _readline(f):
    return f.readline().decode().rstrip('\n')


def imread(f):
    magic = _readline(f)
    if magic not in ['P6']:
        raise NetPBMException("Unknown file format: {}".format(magic))

    width, height = [int(x) for x in _readline(f).split()]
    _ = _readline(f)  # plane range

    data = f.read(width * height * 3)

    return Image(width, height, data)
