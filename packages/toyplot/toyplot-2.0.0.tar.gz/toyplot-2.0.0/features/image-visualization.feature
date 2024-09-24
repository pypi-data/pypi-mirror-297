Feature: Image visualization
    Scenario Outline: Render an image
        Given <image>
        And a default canvas
        And a canvas background color
        When the image is added to the canvas
        Then the figure should match the <reference> reference image

        Examples:
            | image                                   | reference                              |
            | a numpy 1 bit L image                   | image-numpy-1-bit-L                    |
            | a numpy 8 bit L image                   | image-numpy-8-bit-L                    |
            | a numpy 8 bit L image with colormap     | image-numpy-8-bit-L-colormap           |
            | a numpy 8 bit LA image                  | image-numpy-8-bit-LA                   |
            | a numpy 8 bit RGB image                 | image-numpy-8-bit-RGB                  |
            | a numpy 8 bit RGBA image                | image-numpy-8-bit-RGBA                 |
            | a pillow 8 bit L image                  | image-numpy-8-bit-L                    |
            | a pillow 8 bit L image with colormap    | image-numpy-8-bit-L-colormap           |
            | a pillow 8 bit RGB image                | image-numpy-8-bit-RGB                  |
            | a pillow 8 bit RGBA image               | image-numpy-8-bit-RGBA                 |
            | a non-square numpy 8 bit L image                   | image-non-square-numpy-8-bit-L                    |
            | a non-square numpy 8 bit L image with colormap     | image-non-square-numpy-8-bit-L-colormap           |

