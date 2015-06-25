import cv2
import scipy as sp
from math import atan, degrees



def find(image):
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.blur(gray, (3, 3))
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    gradx = cv2.Sobel(gray, ddepth=cv2.cv.CV_32F, dx=1, dy=0, ksize=-1)
    grady = cv2.Sobel(gray, ddepth=cv2.cv.CV_32F, dx=0, dy=1, ksize=-1)

    gradient = cv2.subtract(gradx, grady)
    gradient = cv2.convertScaleAbs(gradient)
    cv2.imwrite("grad.png", gradient)

    (cnts, _) = cv2.findContours(gradient.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

    rect = cv2.minAreaRect(c)

    # box = sp.int0(cv2.cv.BoxPoints(rect))
    # cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)

    return sp.int0(cv2.cv.BoxPoints(rect))


def rotate(file_name):
    box = find(file_name)
    m = sp.argmin(sp.sum(box, 1), 0)
    img = cv2.imread(file_name, 0)
    rows, cols = img.shape
    angle = degrees(atan(float((box[m, 0] - box[m-1, 0]))/(box[m-1, 1] - box[m, 1])))
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite("temp.png", dst)

