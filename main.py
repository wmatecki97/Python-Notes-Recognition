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
minimumDistanceBetweenLines = 4
font = cv2.FONT_HERSHEY_SIMPLEX  # wybór czcionki - musi być z tych FONT_HERSHEY bo inaczej się sypie np. dla Ariala
storeImage = True
useCamera = False
imagePath = './Notes/notes03.jpg'

# Dodawanie czcionki: https://www.youtube.com/watch?v=U6uIrq2eh_o
def main():
    cap = cv2.VideoCapture(0)

    if(useCamera):
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            processImage(frame, gray)

            if cv2.waitKey(500) & 0xFF == ord('q'):
                return
    else:
        img, gray = GetImage()
        processImage(img, gray)
        cv2.waitKey(50000)


def processImage(frame, gray):
    img, areLinesOnImage = GetRotatedImage(frame, gray)
    lines, distanceBetweenLines = GetGrouped5Lines(img)

    if (lines is not None):
        # DrawLines(img, lines)
        notes = GetCircles(img, distanceBetweenLines)
        for note in notes:
            tone = GetTone(lines, distanceBetweenLines, note[1])
            cv2.putText(img, tone, (int(note[0] + distanceBetweenLines), int(note[1])), font, 0.5, (255, 0, 0), 1,
                        cv2.LINE_AA)
    else:
        cv2.putText(img, 'NIE ZNALAZLEM NUT', (100,100), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    cv2.imshow('frame',img)
    if (storeImage):
        cv2.imwrite('notesDescribed.jpg', img)


def GetImage():
    img = cv2.imread(imagePath)
    gray = rgb2gray(img)
    return img, gray


if __name__ == '__main__':
    main();
