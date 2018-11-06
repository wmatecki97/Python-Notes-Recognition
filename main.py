from __future__ import division
from LinesDetection import *
from ToneDetection import GetTone
import cv2
from skimage.color import rgb2gray
from skimage import io

#PARAMETERS
lineLength = 350
minimumDistanceBetweenLines = 4


def main():

    img, areLinesOnImage = GetRotatedImage()

    tone = 'Tutaj pojawi się nazwa dźwięku, który ma środek na wysokości 349px'
    if(areLinesOnImage):
        lines, distanceBetweenLines = GetGrouped5Lines(img)
        DrawLines(img, lines)
        tone = GetTone(lines,distanceBetweenLines,349)

    io.imshow(img)
    axis('off')
    plt.show()

def GetImage():
    img = cv2.imread('./Notes/notes02.jpg')
    gray = rgb2gray(img)
    return img, gray


if __name__ == '__main__':
    main();
