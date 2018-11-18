from __future__ import division

from LinesDetection import *
from ToneDetection import GetTone
from CirclesDetection import *
import cv2
from skimage.color import rgb2gray
from skimage import io
import numpy as np

#PARAMETERS
lineLength = 200
minimumDistanceBetweenLines =  8
maximumDistanceBetweenLines = 50
font = cv2.FONT_HERSHEY_SIMPLEX  # wybór czcionki - musi być z tych FONT_HERSHEY bo inaczej się sypie np. dla Ariala
storeImage = True
useCamera = True
processVideo = False
imagePath = './Notes/notes07.jpg'
videoPath = './Notes/video02.mp4'
drawLines = True
drawAllLines = True
reduceNoise = False
drawContours=False

# Dodawanie czcionki: https://www.youtube.com/watch?v=U6uIrq2eh_o
def main():
    if(processVideo):
        cap = cv2.VideoCapture(videoPath)
    else:
        cap = cv2.VideoCapture(0)


    if(useCamera or processVideo):
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if(reduceNoise):
                frame = cv2.fastNlMeansDenoisingColored(frame,None,4,4,7,10)
            if (storeImage):
                cv2.imwrite('Czysty.jpg', frame)
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            processImage(frame, gray, drawLines, drawAllLines, storeImage, drawContours)

            if (storeImage):
                cv2.imwrite('ZNutkami.jpg', frame)
            if cv2.waitKey(500) & 0xFF == ord('q'):
                return
    else:
        img, gray = GetImage()
        if (storeImage):
                cv2.imwrite('Czysty.jpg', img)
        processImage(img, gray, drawLines, drawAllLines, storeImage, drawContours)

        cv2.waitKey(50000)


def processImage(frame, gray, drawLines, drawAllLines, storeImage, drawContours):
    img, areLinesOnImage = GetRotatedImage(frame, gray)
    lines, distanceBetweenLines = GetGrouped5Lines(img, drawAllLines)

    if (lines is not None):
        if(drawLines):
            DrawLines(img, lines)
        notes = GetCircles(img, distanceBetweenLines, drawContours)
        for note in notes:
            tone = GetTone(lines, distanceBetweenLines, note[1])
            cv2.putText(img, tone, (int(note[0] + distanceBetweenLines), int(note[1])), font, 0.5, (255, 0, 0), 1,
                        cv2.LINE_AA)
    else:
        cv2.putText(img, 'NIE ZNALAZLEM NUT', (100,100), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    cv2.imshow('frame',img)
    if (storeImage):
                cv2.imwrite('ZNutkami.jpg', img)
    # plt.imshow(img)
    # plt.show()


def GetImage():
    img = cv2.imread(imagePath)
    gray = rgb2gray(img)
    return img, gray


if __name__ == '__main__':
    main();
