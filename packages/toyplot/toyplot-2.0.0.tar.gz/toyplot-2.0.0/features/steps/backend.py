# Copyright 2014, Sandia Corporation. Under the terms of Contract
# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains certain
# rights in this software.

from behave import *

import importlib
import io
import numpy
import os
import xml.etree.ElementTree as xml

import test
import testing

if not os.path.exists(testing.backend_dir):
    os.makedirs(testing.backend_dir)

@given(u'that the {} backend is available')
def step_impl(context, name):
    try:
        context.name = name
        context.backend = importlib.import_module(name)
    except:
        context.scenario.skip(reason="The %s backend is not available." % name)


@then(u'the canvas can be rendered to an html file')
def step_impl(context):
    target = os.path.join(testing.backend_dir, "%s.html" % context.name)
    context.backend.render(context.canvas, target)
    #html = xml.parse(target)
    #test.assert_equal(html.getroot().tag, "{http://www.w3.org/2000/svg}svg")


@then(u'the canvas can be rendered to an html buffer')
def step_impl(context):
    buffer = io.BytesIO()
    context.backend.render(context.canvas, buffer)
    #html = xml.parse(buffer.getvalue())
    #test.assert_equal(html.getroot().tag, "html")


@then(u'the canvas can be rendered to a returned html dom')
def step_impl(context):
    html = context.backend.render(context.canvas)
    test.assert_is_instance(html, xml.Element)
    test.assert_equal(html.tag, "div")


@then(u'the canvas can be rendered to a pdf file')
def step_impl(context):
    target = os.path.join(testing.backend_dir, "%s.pdf" % context.name)
    context.backend.render(context.canvas, target)


@then(u'the canvas can be rendered to a pdf buffer')
def step_impl(context):
    buffer = io.BytesIO()
    context.backend.render(context.canvas, buffer)


@then(u'the canvas can be rendered to a returned pdf document')
def step_impl(context):
    pdf = context.backend.render(context.canvas)


@then(u'the canvas can be rendered to a png file')
def step_impl(context):
    target = os.path.join(testing.backend_dir, "%s.png" % context.name)
    context.backend.render(context.canvas, target)
    image = testing.read_png(target)
    test.assert_equal(image.shape, (600, 600, 4))
    test.assert_equal(image.dtype, "uint8")


@then(u'the canvas can be rendered to a png buffer')
def step_impl(context):
    buffer = io.BytesIO()
    context.backend.render(context.canvas, buffer)
    buffer.seek(0)

    image = testing.read_png(buffer)
    test.assert_equal(image.shape, (600, 600, 4))
    test.assert_equal(image.dtype, "uint8")


@then(u'the canvas can be rendered to a returned png document')
def step_impl(context):
    png = context.backend.render(context.canvas)
    image = testing.read_png(io.BytesIO(png))
    test.assert_equal(image.shape, (600, 600, 4))
    test.assert_equal(image.dtype, "uint8")


@then(u'the canvas can be rendered to a 200 pixel wide png document')
def step_impl(context):
    png = context.backend.render(context.canvas, width="200px")
    image = testing.read_png(io.BytesIO(png))
    test.assert_equal(image.shape, (200, 200, 4))
    test.assert_equal(image.dtype, "uint8")

@then(u'the canvas can be rendered to a 150 pixel high png document')
def step_impl(context):
    png = context.backend.render(context.canvas, height="150px")
    image = testing.read_png(io.BytesIO(png))
    test.assert_equal(image.shape, (150, 150, 4))
    test.assert_equal(image.dtype, "uint8")

@then(u'the canvas can be rendered to a half scale png document')
def step_impl(context):
    png = context.backend.render(context.canvas, scale=0.5)
    image = testing.read_png(io.BytesIO(png))
    test.assert_equal(image.shape, (300, 300, 4))
    test.assert_equal(image.dtype, "uint8")


@then(u'the canvas can be rendered to an svg file')
def step_impl(context):
    target = os.path.join(testing.backend_dir, "%s.svg" % context.name)
    context.backend.render(context.canvas, target)
    svg = xml.parse(target)
    test.assert_equal(svg.getroot().tag, "{http://www.w3.org/2000/svg}svg")


@then(u'the canvas can be rendered to an svg buffer')
def step_impl(context):
    buffer = io.BytesIO()
    context.backend.render(context.canvas, buffer)
    #svg = xml.parse(buffer.getvalue())
    #test.assert_equal(svg.getroot().tag, "svg")


@then(u'the canvas can be rendered to a returned svg dom')
def step_impl(context):
    svg = context.backend.render(context.canvas)
    test.assert_is_instance(svg, xml.Element)
    test.assert_equal(svg.tag, "svg")
