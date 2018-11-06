# wykomentowane biblioteki były używane podczas jakiejść części testów/pomysłów
from __future__ import division
from pylab import *
import skimage as ski
# from skimage import feature
from skimage import data, io, filters, exposure, measure, morphology, transform
# from skimage.filters import rank
# from skimage import util
# from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
# from skimage.filters.edges import convolve
from matplotlib import pylab as plt
import numpy as np

def main():
    images =  data.imread()
    , grayImages = imageRead(18)  # pobranie obrazów

    createPlot(images, grayImages)  # utworzenie wykresu

def imageRead(howMany):
    images = []  # tablica obrazów
    grayImages = []  # tablica obrazów w odcieniach szarości
    for i in range(howMany):
        if i <= 9:
            img = io.imread('http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot0%d.jpg' % i, as_gray=False)
            imgGray = io.imread('http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot0%d.jpg' % i, as_gray=True)
            images.append(img)
            grayImages.append(imgGray)
        else:
            img = io.imread('http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot%d.jpg' % i, as_gray=False)
            imgGray = io.imread('http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot%d.jpg' % i, as_gray=True)
            images.append(img)
            grayImages.append(imgGray)

    return images, grayImages

def createPlot(images, grayImages):
    # ustawienia wykresu
    fig = figure(figsize=(20, 20))
    subplots_adjust(wspace=0, hspace=0)

    # byłem zmuszony przeskalować wszystkie obrazki do jednego wymiaru, ponieważ w przeciwnym przypadku zawsze któryś
    # się nie wyświetlał (zazwyczaj środkowy na dole) i do tego posłużą poniższe zmienne
    height, width = 0, 0

    for i in range(len(images)):
        # pobranie obrazków z tablic
        image = grayImages[i]
        originalImage = images[i]

        #pobranie wymairów obrazka
        h, w = np.shape(image)

        # przypisanie wymiarów na podstawie pierwszego obrazka
        if i == 0:
            height = h
            width = w

        # średnia z wartości macierzy
        average = np.mean(image) * 0.666667

        # przypisanie wartości 0 i 1 poszczególnym pikselom w celu późniejszego znalezienia konturów
        for x in range(h):
            for y in range(w):
                pixcel = originalImage[x][y]
                if pixcel[0] >= 32 and pixcel[1] >= 72 and pixcel[2] >= 112:
                    image[x][y] = 1
                if image[x][y] > average:
                    image[x][y] = 0
                else:
                    image[x][y] = 1

        # utworzenie wykresów i usunięcie osi
        ax = fig.add_subplot(len(images) / 3, 3, i + 1)
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)

        # usuwanie szumu na obrazkach
        image = morphology.closing(image, morphology.disk(15))
        image = morphology.dilation(image, morphology.disk(6))

        # zmiana wymiarów obrazka
        image = transform.resize(image, (height, width))
        originalImage = transform.resize(originalImage, (height, width))

        # znalezienie krawędzi
        edges = measure.find_contours(image, 0)

        # wyrysowanie krawędzi i ustalenie, które będa się wyświetlać
        outputEdges = []
        for edge in edges:
            if len(edge) > 370:
                outputEdges.append(edge)
        for edge in outputEdges:
            ax.plot(edge[:, 1], edge[:, 0], linewidth=1.5)

        # znalezienie środków
        centers = []
        for edge in outputEdges:
            sumX, sumY, numPoint = 0, 0, 0
            for point in edge:
                sumX = sumX + point[1]
                sumY = sumY + point[0]
                numPoint = numPoint + 1
            centers.append([(sumX / numPoint), (sumY / numPoint)])
        for center in centers:
            ax.add_artist(plt.Circle(center, 11, color='white'))

        # wyświetlenie obrazka
        io.imshow(originalImage)

    plt.tight_layout()  # dla bardziej zbitego wykresu
    fig.savefig("127329_Obrazy_I.pdf")  # zapisanie w pliku (można zakomentować i odkomentować linię niżej dla zwyczajnego wyświetlenia)
    # plt.show()  # jakby się chciało wyświetlać poza wysyłaniem do pliku to trzeba odkomentować

if __name__ == '__main__':
    main();
