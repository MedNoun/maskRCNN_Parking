from django.http import HttpResponse
import cv2
import pickle
import cvzone
import numpy as np

width, height = 103, 43
with open('polygons', 'rb') as f:
    posList = pickle.load(f)


def empty(a):
    pass



INDEXES = []

def checkSpaces(imgThres):
    global INDEXES
    spaces = 0
    indexes = []
    for i,pos in enumerate(posList):
        x, y = pos
        w, h = width, height
        imgCrop = imgThres[y:y + h, x:x + w]
        count = cv2.countNonZero(imgCrop)
        indexes.append(0)
        if count < 900:
            spaces += 1
            indexes[i]=1
    INDEXES = indexes
    return (spaces,len(posList))
 

def main():

    cap = cv2.VideoCapture('carPark.mp4')
    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, img = cap.read()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        checkSpaces(imgDilate)
        cv2.imshow("Image", img)
        # cv2.imshow("ImageBlur", imgBlur)
        # cv2.imshow("ImageThres", imgMedian)
        cv2.waitKey(10)

# Create your views here.
def getStatus(request):
    return HttpResponse(INDEXES,content_type="application/json")
def activate(request):
    main()
