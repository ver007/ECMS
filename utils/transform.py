import base64
import cv2
import numpy as np


def transform_img(img):
    img = base64.b64decode(img)
    img = cv2.imdecode(np.asarray(bytearray(img), dtype='uint8'), cv2.IMREAD_COLOR)
    return img
