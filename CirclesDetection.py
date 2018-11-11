from main import *
from skimage import data, color, img_as_ubyte
from skimage.feature import canny
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter
import cv2
import matplotlib.pyplot as plt

# kod wzięty ze strony http://scikit-image.org/docs/dev/auto_examples/edges/plot_circular_elliptical_hough_transform.html
def GetCircles():
    image, gray = GetImage()
    image_rgb = image[0:220, 0:420]
    image_gray = color.rgb2gray(image_rgb)
    edges = canny(image_gray, sigma=2.0,
                  low_threshold=0.55, high_threshold=0.8)

    # Perform a Hough Transform
    # The accuracy corresponds to the bin size of a major axis.
    # The value is chosen in order to get a single high accumulator.
    # The threshold eliminates low accumulators
    result = hough_ellipse(edges)
    result.sort(order='accumulator')

    # Estimated parameters for the ellipse
    best = list(result[-1])
    print(len(result))  # tutaj printuje ile znajduje elips, dzięki czemu widać czemu to tak długo zajmuje
    yc, xc, a, b = [int(round(x)) for x in best[1:5]]
    orientation = best[5]

    # Draw the ellipse on the original image
    cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
    image_rgb[cy, cx] = (0, 0, 255)

    plt.plot(figsize=(4, 4))
    plt.imshow(image_rgb)

    plt.show()