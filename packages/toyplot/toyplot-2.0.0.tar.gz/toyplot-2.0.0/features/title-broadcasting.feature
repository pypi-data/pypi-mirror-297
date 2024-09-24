Feature: Title Broadcasting
    Scenario Outline: Title broadcasting use-cases
        Given a default canvas
        And a set of cartesian axes
        And a set of diverging series
        And a set of per-series title values
        And a set of per-datum title values
        Then <mark> can be rendered with <title>
        And the figure should match the <reference> reference image

        Examples:
            | mark                         | title                            | reference |
            | bars                         | one explicit title               | title-broadcast-bars-one-title |
            | bars                         | per-series titles                | title-broadcast-bars-per-series-titles |
            | bars                         | per-datum titles                 | title-broadcast-bars-per-datum-titles |
            | fills                        | one explicit title               | title-broadcast-fills-one-title |
            | fills                        | per-series titles                | title-broadcast-fills-per-series-titles |
            | hlines                       | one explicit title               | title-broadcast-hlines-one-title |
            | hlines                       | per-datum titles                 | title-broadcast-hlines-per-datum-titles |
            | plots                        | one explicit title               | title-broadcast-plots-one-title |
            | plots                        | per-series titles                | title-broadcast-plots-per-series-titles |
            | plots                        | per datum titles                 | title-broadcast-plots-per-datum-titles |
            | plots                        | per-series and per datum titles  | title-broadcast-plots-per-series-per-datum-titles |
            | rects                        | one explicit title               | title-broadcast-rects-one-title |
            | rects                        | per-datum titles                 | title-broadcast-rects-per-datum-titles |
            | scatterplots                 | one explicit title               | title-broadcast-scatterplots-one-title |
            | scatterplots                 | per-series titles                | title-broadcast-scatterplots-per-series-titles |
            | scatterplots                 | per-datum titles                 | title-broadcast-scatterplots-per-datum-titles |
            | text                         | one explicit title               | title-broadcast-text-one-title |
            | text                         | per-datum titles                 | title-broadcast-text-per-datum-titles |
            | vlines                       | one explicit title               | title-broadcast-vlines-one-title |
            | vlines                       | per-datum titles                 | title-broadcast-vlines-per-datum-titles |

    Scenario: Per-datum title broadcasting with one series
        Given a default canvas
        And a set of cartesian axes
        Then bars can be rendered with a single series and per-datum titles
        And the figure should match the title-broadcast-bars-single-series-per-datum-titles reference image

