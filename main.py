from __future__ import division

from LinesDetection import *
from ToneDetection import GetTone
from CirclesDetection import *
import cv2
from skimage.color import rgb2gray
from skimage import io
import numpy as np

#PARAMETERS
lineLength = 400
minimumDistanceBetweenLines = 4
font = cv2.FONT_HERSHEY_SIMPLEX  # wybór czcionki - musi być z tych FONT_HERSHEY bo inaczej się sypie np. dla Ariala
storeImage = True


# Dodawanie czcionki: https://www.youtube.com/watch?v=U6uIrq2eh_o
def main():

    img, areLinesOnImage = GetRotatedImage()


    if(areLinesOnImage):
        lines, distanceBetweenLines = GetGrouped5Lines(img)
        #DrawLines(img, lines)
        notes = GetCircles(img, distanceBetweenLines)
        for note in notes:
            tone = GetTone(lines,distanceBetweenLines,note[1])
            cv2.putText(img, tone, (int(note[0] + distanceBetweenLines), int(note[1])), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    else:
        cv2.putText(img, 'NIE ZNALAZŁEM NUT', (0,0), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)


    io.imshow(img)
    if(storeImage):
        cv2.imwrite('notesDescribed.jpg', img)
    axis('off')
    plt.show()

def GetImage():
    img = cv2.imread('./Notes/notes03.jpg')
    gray = rgb2gray(img)
    return img, gray


if __name__ == '__main__':
    main();
