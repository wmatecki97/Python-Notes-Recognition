# wykomentowane biblioteki były używane podczas jakiejść części testów/pomysłów
from __future__ import division
from pylab import *
import skimage as ski
# from skimage import feature
from skimage import data, io, filters, exposure, measure, morphology, transform
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
from matplotlib import pylab as plt
import numpy as np
from skimage.filters.edges import convolve
import cv2
import numpy as np

lineLength = 370

def main():
    img, gray =  GetImage()

    GetLines(img)
    plt.show()
    #createPlot(img, gray)  # utworzenie wykresu


def GetLines(img):
    # Convert the img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply edge detection method on the image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # This returns an array of r and theta values
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    for i in range(len(lines)):
        # The below for loop runs till r and theta values
        # are in the range of the 2d array
        for r, theta in lines[i]:
            # Stores the value of cos(theta) in a
            a = np.cos(theta)

            # Stores the value of sin(theta) in b
            b = np.sin(theta)

            # x0 stores the value rcos(theta)
            x0 = a * r

            # y0 stores the value rsin(theta)
            y0 = b * r

            # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
            x1 = int(x0 + 1000 * (-b))

            # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
            y1 = int(y0 + 1000 * (a))

            # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
            x2 = int(x0 - 1000 * (-b))

            # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
            y2 = int(y0 - 1000 * (a))

            # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
            # (0,0,255) denotes the colour of the line to be
            # drawn. In this case, it is red.
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    # All the changes made in the input image are finally
    # written on a new image houghlines.jpg
    cv2.imwrite('linesDetected.jpg', img)


def GetImage():
    img = cv2.imread('./Notes/notes1.jpg')
    gray = rgb2gray(img)
    return img, gray


if __name__ == '__main__':
    main();
