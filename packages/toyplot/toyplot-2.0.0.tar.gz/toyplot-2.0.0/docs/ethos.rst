
.. image:: ../artwork/toyplot.png
  :width: 200px
  :align: right

.. _ethos:

The Toyplot Ethos
=================

    | *Always look your best.*
    | *Share your things.*
    | *Play well with others.*
    | *Never tell a lie.*

What began as a quick workaround to produce better figures for some experiments
in machine learning has quickly grown into Toyplot, "the kid-sized plotting toolkit with
grownup-sized goals".  In a nutshell, we think that scientists and engineers
should expect more from their plots, from explicit support for
reproducibility and open science to greater clarity and better aesthetics.

We especially feel that, in an age of ubiquitous electronic media and the web,
it makes little sense to publish using media (like PDF) designed to mimic
the limitations of static paper.  Toyplot embraces the standards of the internet - HTML,
SVG, and Javascript - as its primary medium, so we can make useful new
interactions part of the everyday experiences of data graphic users.  Because
we're passionate about publishing and sharing results, Toyplot graphics will always be
completely self-contained and embeddable, without the need for a server.  All
of the Toyplot graphics you will see in this documentation are live and
interactive, despite the fact that they were created offline in a Jupyter
notebook and passed through several publishing steps on the way to becoming our
documentation.  Of course, we provide backends to publish Toyplot figures to
legacy formats including PDF, PNG, and MP4 *(Play well with others)*.

With most toolkits, interactivity means throwaway features like pan-and-zoom.  For
Toyplot, we're exploring simple-but-effective ideas to address the questions a
colleague might ask when viewing a graphic in the real world: "What's the value
at this weird peak?" "Where do those two series cross?" "Can I get a copy of the data?"
We're working on efficient animation that doesn't compromise the quality of your graphic
with compression artifacts; and interactive data cursors that display quantities
of interest and descriptive statistics just by hovering the mouse.  And since
the raw data is already implicitly embedded in a graphic, why not support
reproducibility by making it easy to export, so the viewer can work with it
themselves?  That's why Toyplot figures can export their underlying raw data
in CSV format *(Share your things)*.

Last but definitely not least: Toyplot fully embraces principles and best
practices for clarity and aesthetics in data graphics that are well-established
by the visualization community, yet sadly lacking in contemporary plotting
libraries *(Always look your best)*.  Toyplot has beautiful color palettes and sensible default styling
that minimize chartjunk and maximize data ink out of the box, not as
afterthoughts or addons.

