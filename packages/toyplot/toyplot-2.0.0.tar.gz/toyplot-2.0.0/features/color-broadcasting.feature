Feature: Color Broadcasting
    Scenario Outline: Color broadcasting use-cases
        Given a default canvas
        And a set of cartesian axes
        And a set of diverging series
        And a set of per-series values
        And a set of per-series colors
        And a set of per-datum values
        And a set of per-datum colors
        Then <mark> can be rendered with <color>
        And the figure should match the <reference> reference image

        Examples:
            | mark             | color                                       | reference |
            | bars             | default colors                              | color-broadcast-bars-default |
            | bars             | one explicit color                          | color-broadcast-bars-one-color |
            | bars             | per-series explicit colors                  | color-broadcast-bars-per-series-colors |
            | bars             | per-datum explicit colors                   | color-broadcast-bars-per-datum-colors |
            | bars             | colormap colors                             | color-broadcast-bars-colormap |
            | bars             | per-series value colors                     | color-broadcast-bars-per-series-values |
            | bars             | per-series value + colormap colors          | color-broadcast-bars-per-series-values-colormap |
            | bars             | per-datum value colors                      | color-broadcast-bars-per-datum-values |
            | bars             | per-datum value + colormap colors           | color-broadcast-bars-per-datum-values-colormap |
            | fills            | default colors                              | color-broadcast-fills-default |
            | fills            | one explicit color                          | color-broadcast-fills-one-color |
            | fills            | per-series explicit colors                  | color-broadcast-fills-per-series-colors |
            | fills            | colormap colors                             | color-broadcast-fills-colormap |
            | fills            | per-series value colors                     | color-broadcast-fills-per-series-values |
            | fills            | per-series value + colormap colors          | color-broadcast-fills-per-series-values-colormap |
            | hlines           | default colors                              | color-broadcast-hlines-default |
            | hlines           | one explicit color                          | color-broadcast-hlines-one-color |
            | hlines           | per-datum explicit colors                   | color-broadcast-hlines-per-datum-colors |
            | hlines           | colormap colors                             | color-broadcast-hlines-colormap |
            | hlines           | per-datum value colors                      | color-broadcast-hlines-per-datum-values |
            | hlines           | per-datum value + colormap colors           | color-broadcast-hlines-per-datum-values-colormap |
            | plots            | default colors                              | color-broadcast-plots-default |
            | plots            | one explicit color                          | color-broadcast-plots-one-color |
            | plots            | per-series explicit colors                  | color-broadcast-plots-per-series-colors |
            | plots            | colormap colors                             | color-broadcast-plots-colormap |
            | plots            | per-series value colors                     | color-broadcast-plots-per-series-values |
            | plots            | per-series value + colormap colors          | color-broadcast-plots-per-series-values-colormap |
            | plots            | default marker colors                       | color-broadcast-plots-marker-default |
            | plots            | one explicit marker color                   | color-broadcast-plots-one-marker-color |
            | plots            | per-series explicit marker colors           | color-broadcast-plots-per-series-marker-colors |
            | plots            | colormap marker colors                      | color-broadcast-plots-colormap-marker |
            | plots            | per-series value marker colors              | color-broadcast-plots-per-series-values-marker |
            | plots            | per-series value + colormap marker colors   | color-broadcast-plots-per-series-values-colormap-marker |
            | plots            | per-datum value marker colors               | color-broadcast-plots-per-datum-values-marker |
            | plots            | per-datum value + colormap marker colors    | color-broadcast-plots-per-datum-values-colormap-marker |
            | rects            | default colors                              | color-broadcast-rects-default |
            | rects            | one explicit color                          | color-broadcast-rects-one-color |
            | rects            | per-datum explicit colors                   | color-broadcast-rects-per-datum-colors |
            | rects            | colormap colors                             | color-broadcast-rects-colormap |
            | rects            | per-datum value colors                      | color-broadcast-rects-per-datum-values |
            | rects            | per-datum value + colormap colors           | color-broadcast-rects-per-datum-values-colormap |
            | scatterplots     | default colors                              | color-broadcast-scatterplots-default |
            | scatterplots     | one explicit color                          | color-broadcast-scatterplots-one-color |
            | scatterplots     | per-series explicit colors                  | color-broadcast-scatterplots-per-series-colors |
            | scatterplots     | per-datum explicit colors                   | color-broadcast-scatterplots-per-datum-colors |
            | scatterplots     | colormap colors                             | color-broadcast-scatterplots-colormap |
            | scatterplots     | per-series value colors                     | color-broadcast-scatterplots-per-series-values |
            | scatterplots     | per-series value + colormap colors          | color-broadcast-scatterplots-per-series-values-colormap |
            | scatterplots     | per-datum value colors                      | color-broadcast-scatterplots-per-datum-values |
            | scatterplots     | per-datum value + colormap colors           | color-broadcast-scatterplots-per-datum-values-colormap |
            | text             | default colors                              | color-broadcast-text-default |
            | text             | one explicit color                          | color-broadcast-text-one-color |
            | text             | per-datum explicit colors                   | color-broadcast-text-per-datum-colors |
            | text             | colormap colors                             | color-broadcast-text-colormap |
            | text             | per-datum value colors                      | color-broadcast-text-per-datum-values |
            | text             | per-datum value + colormap colors           | color-broadcast-text-per-datum-values-colormap |
            | vlines           | default colors                              | color-broadcast-vlines-default |
            | vlines           | one explicit color                          | color-broadcast-vlines-one-color |
            | vlines           | per-datum explicit colors                   | color-broadcast-vlines-per-datum-colors |
            | vlines           | colormap colors                             | color-broadcast-vlines-colormap |
            | vlines           | per-datum value colors                      | color-broadcast-vlines-per-datum-values |
            | vlines           | per-datum value + colormap colors           | color-broadcast-vlines-per-datum-values-colormap |

    Scenario Outline: Color broadcasting types
        Given a default canvas
        And a set of cartesian axes
        And a set of diverging series
        Then <mark> can be rendered with <type>
        And the figure should match the <reference> reference image

        Examples:
            | mark             | type                                        | reference |
            | bars             | an array of CSS colors                      | color-broadcast-css-array |
