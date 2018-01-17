from nose.tools import assert_equal
from main import render_rectangle, Rectangle
from netpbm import Image

WHITE = (0xff, 0xff, 0xff)

def test_easy():
    img = Image(2, 2)
    r = Rectangle(0, 0, 2, 2, WHITE)
    render_rectangle(r, img)
    assert_equal(img.data, b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')

def test_zero_height():
    img = Image(2, 2)
    r = Rectangle(0, 0, 2, 0, WHITE)
    render_rectangle(r, img)
    assert_equal(img.data, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

def test_zero_width():
    img = Image(2, 2)
    r = Rectangle(0, 0, 0, 2, WHITE)
    render_rectangle(r, img)
    assert_equal(img.data, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
