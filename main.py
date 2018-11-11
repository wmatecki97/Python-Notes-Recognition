from __future__ import division

from LinesDetection import *
from ToneDetection import GetTone
from CirclesDetection import *
import cv2
from skimage.color import rgb2gray
from skimage import io
import numpy as np

#PARAMETERS
lineLength = 350
minimumDistanceBetweenLines = 4
font = cv2.FONT_HERSHEY_SIMPLEX  # wybór czcionki - musi być z tych FONT_HERSHEY bo inaczej się sypie np. dla Ariala

# Może się przydać (trafiłem podczas szukania):
# https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/
# https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/

# Dodawanie czcionki: https://www.youtube.com/watch?v=U6uIrq2eh_o
def main():
    # GetCircles()  # to trzeba odkomentować do szukania owali, ale wtedy trzeba resztę maina zakomentować...

    img, areLinesOnImage = GetRotatedImage()

    tone = 'Tutaj pojawi się nazwa dźwięku, który ma środek na wysokości 349px'
    if(areLinesOnImage):
        lines, distanceBetweenLines = GetGrouped5Lines(img)
        DrawLines(img, lines)
        tone = GetTone(lines,distanceBetweenLines,349)

    # zamiast (0, 130), wystarczy wprowadzić odpowiednie współrzędne i tam się tekst wyświetli)
    cv2.putText(img, 'Text', (0, 130), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
    io.imshow(img)
    axis('off')
    plt.show()

def GetImage():
    img = cv2.imread('./Notes/notes1.jpg')
    gray = rgb2gray(img)
    return img, gray


if __name__ == '__main__':
    main();
