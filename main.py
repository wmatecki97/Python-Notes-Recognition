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

# Dodawanie czcionki: https://www.youtube.com/watch?v=U6uIrq2eh_o
def main():

    img, areLinesOnImage = GetRotatedImage()

    tone = 'Tutaj pojawi się nazwa dźwięku, który ma środek na wysokości 349px'
    if(areLinesOnImage):
        lines, distanceBetweenLines = GetGrouped5Lines(img)
        #DrawLines(img, lines)
        notes = GetCircles(img, distanceBetweenLines)
        for note in notes:
            tone = GetTone(lines,distanceBetweenLines,note[1])
            cv2.putText(img, tone, (int(note[0] + distanceBetweenLines), int(note[1])), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)


    # zamiast (0, 130), wystarczy wprowadzić odpowiednie współrzędne i tam się tekst wyświetli)
    io.imshow(img)
    cv2.imwrite('notesDescribed.jpg', img)
    axis('off')
    plt.show()

def GetImage():
    img = cv2.imread('./Notes/notes03.jpg')
    gray = rgb2gray(img)
    return img, gray


if __name__ == '__main__':
    main();
