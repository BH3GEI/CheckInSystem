import cv2
import imutils
import numpy as np
import math
#幂律变换 φ>1
image = cv2.imread('data/jm/6.jpg')
gamma_img1 = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.float32)
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        gamma_img1[i, j, 0] = math.pow(image[i, j, 0], 5)
        gamma_img1[i, j, 1] = math.pow(image[i, j, 1], 5)
        gamma_img1[i, j, 2] = math.pow(image[i, j, 2], 5)
cv2.normalize(gamma_img1, gamma_img1, 0, 255, cv2.NORM_MINMAX)
gamma_img1 = cv2.convertScaleAbs(gamma_img1)
cv2.imshow('image', imutils.resize(image, 800))
cv2.imshow('gamma1 transform', imutils.resize(gamma_img1, 800))
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
