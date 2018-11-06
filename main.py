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
import math

lineLength = 370
minimumDistanceBetweenLines = 3

def main():

    img = GetRotatedImage()
    lines, alfa = GetLines(img)
    GetLinesYPositions(lines)

    DrawLines(img, lines)
    io.imshow(img)
    axis('off')
    plt.show()
    #createPlot(img, gray)  # utworzenie wykresu


def GetLinesYPositions(lines):
    linesYPosition = []
    for i in range(len(lines)):
        linesYPosition.append(lines[i][1])
    linesYPosition.sort()
    i = 0
    while (i < len(linesYPosition) - 1):
        if (linesYPosition[i + 1] - linesYPosition[i] < minimumDistanceBetweenLines):
            avg = (linesYPosition[i] + linesYPosition[i + 1]) / 2
            linesYPosition.remove(linesYPosition[i + 1])
            linesYPosition.insert(i, avg)
            linesYPosition.remove(linesYPosition[i + 1])
        i = i + 1
    distances = []
    for i in range(len(linesYPosition) - 1):
        distances.append(abs(linesYPosition[i] - linesYPosition[i + 1]))


def GetRotatedImage():
    img, gray =  GetImage()
    lines, alfa = GetLines(img)
    alfa = math.degrees(alfa) -90
    cols = len(img[0])
    rows = len(img)
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), alfa, 1)
    t = cv2.warpAffine(img, M, (cols, int(rows * math.cos(math.radians(alfa)))))
    return t


def DrawLines(img, lines):

    for i in range(len(lines)):
        cv2.line(img, (lines[i][0], lines[i][1]), (lines[i][2], lines[i][3]), (0, 0, 255), 2)

    # All the changes made in the input image are finally
    # written on a new image houghlines.jpg
    cv2.imwrite('linesDetected.jpg', img)

def GetLines(img):

    result = []
    alfas = []
    # Convert the img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply edge detection method on the image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # This returns an array of r and theta values
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    for i in range(len(lines)):
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

            result.append([x1,y1,x2,y2])
            alfas.append(theta)
    alfas.sort()
    alfa = alfas[int(len(alfas)/2)]
    a= result[0][0]
    return result, alfa

def GetImage():
    img = cv2.imread('./Notes/notes1.jpg')
    gray = rgb2gray(img)
    return img, gray


if __name__ == '__main__':
    main();
