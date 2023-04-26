import cv2
import imutils as imutils
import numpy as np

rgb_image = cv2.imread('data/jm/1.jpg', 1)
gray_image = cv2.imread('data/jm/1.jpg', 0)
hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
gray2_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
cv2.imshow('origin image', imutils.resize(rgb_image, 200))  # 利用imutils模块调整显示图像大小
cv2.imshow('gray image', imutils.resize(gray_image, 200))
cv2.imshow('hsv image', imutils.resize(hsv_image, 200))  # 利用imutils模块调整显示图像大小
cv2.imshow('gray2 image', imutils.resize(gray2_image, 200))

# cv2.circle(image, center, radius, color, thickness, lineType)
# cv2.rectangle(image, top-left, bottom-right, color, thickness, lineType)
img = np.ones((512, 512, 3), np.uint8)
img = 255*img
img = cv2.line(img, (100, 100), (400, 400), (255, 0, 0), 5)
img = cv2.rectangle(img, (200, 20), (400, 120), (0, 255, 0), 3)
img = cv2.circle(img, (100, 400), 50, (0, 0, 255), 2)
img = cv2.circle(img, (250, 400), 50, (0, 0, 255), 0)
img = cv2.ellipse(img, (256, 256), (100, 50), 0, 0, 180, (0, 255, 255), -1)
pts = np.array([[10, 5], [20, 30], [70, 20], [50, 10]], np.int32)
img = cv2.polylines(img, [pts], True, (0, 0, 0), 2)
cv2.imshow('img', img)


if cv2.waitKey(0) == ord('A'):
    cv2.destroyAllWindows()