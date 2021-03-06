from main import *
from pylab import *
import random
import cv2
import numpy as np
import math


def DrawAllLinesByYPosition(img, linesYPositions):

    for i in range(len(linesYPositions)):
        cv2.line(img, (0, int(linesYPositions[i])), (len(img[0]), int(linesYPositions[i])), (0,0,255), 2)
    # All the changes made in the input image are finally
    # written on a new image houghlines.jpg
    cv2.imwrite('linesDetected.jpg', img)

def GetGrouped5Lines(img, drawAllLines):
    lines, alfa, areLinesOnImage = GetLines(img)
    if(lines is not None):
        if(drawAllLines):
            DrawAllLines(img, lines)

        linesYPositions, distanceBetweenLines = GetLinesYPositions(lines)

        if(drawAllLines):
            DrawAllLinesByYPosition(img, linesYPositions)

        if(len(linesYPositions)>4):
            return Group5Lines(linesYPositions, distanceBetweenLines), distanceBetweenLines

    return None, None

# Returns list of Y Positions of horizontal lines
# Returns dominant as most common distance between lines in pixels
def GetLinesYPositions(lines):
    linesYPosition = []
    allYPositions = []
    # Get Y Position Value from line
    for i in range(len(lines)):
        if(abs(lines[i][1] - lines[i][3]) < 2): #only horizontal lines
            allYPositions.append(lines[i][1])
    allYPositions.sort()

    i = 0
    sameY = []
    last = len(allYPositions) - 1
    # delete intermediate lines if they are too close
    while i <= last:
        distance = minimumDistanceBetweenLines

        if(i<last):
            distance = allYPositions[i + 1] - allYPositions[i]

        sameY.append(i)

        if distance >= minimumDistanceBetweenLines:
            sum = 0
            for j in range(len(sameY)):
                sum = sum + allYPositions[sameY[j]]
            position = sum/len(sameY)
            linesYPosition.append(position)
            sameY=[]
            if(i==last-1):
                linesYPosition.append(allYPositions[last])
        i = i + 1
    distances = []

    if(len(linesYPosition) > 4):
        for i in range(len(linesYPosition) - 1):
            distances.append(abs(linesYPosition[i] - linesYPosition[i + 1]))

        dominant = max(set(distances), key=distances.count)
        if(dominant>maximumDistanceBetweenLines):
            dominant = maximumDistanceBetweenLines;
        return linesYPosition, dominant
    return [],[]


def Group5Lines(listOfLines, distanceBetweenLines):


    result =[]
    group = []
    for i in range(len(listOfLines)):
        if(len(group) == 5):
            firstDistance = group[1]-group[0]
            lastDistance = listOfLines[i] -group[4]
            if(firstDistance > lastDistance):
                group.remove(group[0])
            else:
                result.append(group)
                group = []
        group.append(listOfLines[i])
        if(i == len(listOfLines)-1 or abs(listOfLines[i + 1] - listOfLines[i]) > distanceBetweenLines*1.3):
            if(len(group) > 2):
                while(len(group) < 5): #When not all lines was found try to create imitation
                    group.append(group[len(group)-1] + distanceBetweenLines)
                result.append(group)
            group = []
    return result


def GetRotatedImage(img, gray):
    #img, gray =  GetImage()
    lines, alfa, areLinesOnImage = GetLines(img)
    if(areLinesOnImage):
        alfa = math.degrees(alfa) -90
        cols = len(img[0])
        rows = len(img)
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), alfa, 1)
        t = cv2.warpAffine(img, M, (cols, int(rows * math.cos(math.radians(alfa)))))
        return t, True
    return img, False


def DrawAllLines(img, lines):

    for i in range(len(lines)):
            #for j in range(len(lines[i])):
            x1 = lines[i][0]
            y1 = lines[i][1]
            x2 = lines[i][2]
            y2 = lines[i][3]
            cv2.line(img, (lines[i][0], lines[i][1]), (lines[i][2], lines[i][3]), [255,0,0], 1)

    # All the changes made in the input image are finally
    # written on a new image houghlines.jpg
    cv2.imwrite('linesDetected.jpg', img)


def DrawLines(img, groupedLinesYPositions):

    for i in range(len(groupedLinesYPositions)):
        colour = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        for j in range(len(groupedLinesYPositions[i])):
            cv2.line(img, (0, int(groupedLinesYPositions[i][j])), (len(img[0]), int(groupedLinesYPositions[i][j])), colour, 2)

    # All the changes made in the input image are finally
    # written on a new image houghlines.jpg
    cv2.imwrite('linesDetected.jpg', img)


def GetLines(img):

    result = []
    alfas = []
    # from https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/

    # Convert the img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply edge detection method on the image
    edges = cv2.Canny(gray, 50, 150)
    # This returns an array of r and theta values
    lines = cv2.HoughLines(edges, 1, np.pi / 180, lineLength)
    if(not lines is None):
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
        alfa = alfas[int(len(alfas)/2)]  #median from angle between horizontal line and image lines
        return result, alfa, True
    return None, None, False
