# Copyright 2014, Sandia Corporation. Under the terms of Contract
# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains certain
# rights in this software.

from behave import *

import test
import numpy
import sys
import toyplot.browser
import unittest.mock
import webbrowser


@given(u'a sample Toyplot canvas, the canvas can be displayed in a web browser')
def step_impl(context):
    canvas, axes, mark = toyplot.plot(numpy.sin(numpy.linspace(0, 10)))
    with unittest.mock.patch("webbrowser.open") as webbrowser_open:
        toyplot.browser.show(canvas)
    test.assert_equal(webbrowser_open.call_count, 1)
    test.assert_true(
        webbrowser_open.call_args[0][0].startswith("file://"))
    test.assert_equal(webbrowser_open.call_args[1]["new"], 1)
    test.assert_equal(webbrowser_open.call_args[1]["autoraise"], True)


