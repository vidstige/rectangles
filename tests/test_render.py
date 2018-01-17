from nose.tools import assert_equal
from main import render_rectangle, Rectangle
from netpbm import Image

WHITE = (0xff, 0xff, 0xff)

def test_easy():
    img = Image(2, 2)
    r = Rectangle(0, 0, 2, 2, WHITE)
    render_rectangle(r, img)
    assert_equal(img.data,
                 [255, 255, 255, 255, 255, 255,
                  255, 255, 255, 255, 255, 255])

def test_half_x():
    img = Image(3, 2)
    r = Rectangle(0.5, 0, 2, 2, WHITE)
    render_rectangle(r, img)
    assert_equal(img.data,
                 [127.5, 127.5, 127.5, 255, 255, 255, 127.5, 127.5, 127.5,
                  127.5, 127.5, 127.5, 255, 255, 255, 127.5, 127.5, 127.5])

def test_zero_height():
    img = Image(2, 2)
    r = Rectangle(0, 0, 2, 0, WHITE)
    render_rectangle(r, img)
    assert_equal(img.data,
                 [0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0])

def test_zero_width():
    img = Image(2, 2)
    r = Rectangle(0, 0, 0, 2, WHITE)
    render_rectangle(r, img)
    assert_equal(img.data,
                 [0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0])
