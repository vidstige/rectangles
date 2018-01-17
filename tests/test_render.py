from nose.tools import assert_equal
from main import render_rectangle, Rectangle
from netpbm import Image

WHITE = (0xff, 0xff, 0xff)

def test_easy():
    img = Image(2, 2)
    r = Rectangle(0, 0, 2, 2, WHITE)
    render_rectangle(r, img)
    assert_equal(img.data, b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
