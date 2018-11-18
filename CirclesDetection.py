from main import *
from skimage import data, color, morphology, img_as_ubyte, measure
from skimage.feature import canny
from skimage.transform import hough_ellipse, hough_circle
from skimage.draw import ellipse_perimeter
import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2gray


def GetCircles(image_rgb, maxNoteHeight, drawContours):
    # image_rgb = image[0:220, 0:420]
    image_gray = rgb2gray(image_rgb)

    edges = canny(image_gray, sigma=2.0,
                  low_threshold=0.25, high_threshold=0.2)

    edges = morphology.dilation(edges)
    edges = morphology.dilation(edges)
    edges = morphology.closing(edges)
    #plt.imshow(image_rgb)
    contours = measure.find_contours(edges,0)

    #plt.imshow(contours)
    circles=[]
    for n, contour in enumerate(contours):
        area = getArea(contour)
        plt.plot(contour[:, 1], contour[:, 0], linewidth=2)
        if(area < maxNoteHeight**2*1.5 and len(contour[0]) < maxNoteHeight and area > (maxNoteHeight*0.8)**2):
            circles.append(contour)

    centers =[]
    for circle in circles:
        sumX, sumY, numPoint = 0,0,0
        for point in circle:
            sumX = sumX + point[1]
            sumY = sumY + point[0]
            numPoint = numPoint+1
        centers.append([sumX/numPoint, sumY/numPoint])

    if(drawContours):
        plt.imshow(image_rgb)

        for n, circle in enumerate(circles):
            plt.plot(circle[:, 1], circle[:, 0], linewidth=2)

        plt.show()
    return centers

def getArea(contour):
    columns = 0;
    for row in contour:
        if (len(row) > columns):
            columns = len(row)
    area = columns * len(contour)
    return area
