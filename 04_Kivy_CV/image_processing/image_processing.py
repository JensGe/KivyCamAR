import cv2
# import imutils
import numpy as np


def simple_return(image):
    return image


def crop_image(image):
    return image[0:350, 0:350]


detector = cv2.CascadeClassifier('image_processing/cascades/haarcascade_frontalface_default.xml')


def face_detection(image, rect_color, rotation):

    if rotation == 90:
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if rotation == -90:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    orig_image = image.copy()
    height, width = orig_image.shape[:2]

    new_width = 300
    r = new_width / float(width)
    dim = (new_width, int(height * r))
    ratio = (width / dim[0], height / dim[1])
    image = cv2.resize(image, dim)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceRects = detector.detectMultiScale(image, scaleFactor=1.2, minNeighbors=5,
                                          minSize=(20, 20), flags=cv2.CASCADE_SCALE_IMAGE)

    for (x, y, w, h) in faceRects:
        x = int(x * ratio[0])
        y = int(y * ratio[1])
        w = x + int(w * ratio[0])
        h = y + int(h * ratio[1])
        cv2.rectangle(orig_image, (x, y), (w, h), rect_color, 2)

    if rotation == 90:
        orig_image = cv2.rotate(orig_image, cv2.ROTATE_90_CLOCKWISE)
    if rotation == -90:
        orig_image = cv2.rotate(orig_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    return orig_image, faceRects
