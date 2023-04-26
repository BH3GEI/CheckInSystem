import cv2
import random
import imutils
import numpy as np
# 做的是整体增强
# 彩色图像每个像素值是[x,y,z], 灰度图像每个像素值便是一个np.uint8
image = cv2.imread('data/jm/6.jpg')
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 图像大小调整
ori_h, ori_w = image.shape[:2]
height, width = gray_img.shape[:2]
image = cv2.resize(image, (int(ori_w / ori_h * 400), 400), interpolation=cv2.INTER_CUBIC)
gray_img = cv2.resize(gray_img, (int(width / height * 400), 400), interpolation=cv2.INTER_CUBIC)

# a<0 and b=0: 图像的亮区域变暗，暗区域变亮
a, b = -0.5, 0
new_img1 = np.ones((gray_img.shape[0], gray_img.shape[1]), dtype=np.uint8)
for i in range(new_img1.shape[0]):
    for j in range(new_img1.shape[1]):
        new_img1[i][j] = gray_img[i][j] * a + b

# a>1: 增强图像的对比度,图像看起来更加清晰
a, b = 1.5, -200
new_img2 = np.ones((gray_img.shape[0], gray_img.shape[1]), dtype=np.uint8)
for i in range(new_img2.shape[0]):
    for j in range(new_img2.shape[1]):
        if gray_img[i][j] * a + b > 255:
            new_img2[i][j] = 255
        else:
            new_img2[i][j] = gray_img[i][j] * a + b

# a<1: 减小了图像的对比度, 图像看起来变暗
a, b = 0.5, 0
new_img3 = np.ones((gray_img.shape[0], gray_img.shape[1]), dtype=np.uint8)
for i in range(new_img3.shape[0]):
    for j in range(new_img3.shape[1]):
        new_img3[i][j] = gray_img[i][j] * a + b

# a=1且b≠0, 图像整体的灰度值上移或者下移, 也就是图像整体变亮或者变暗, 不会改变图像的对比度
a, b = 1, -50
new_img4 = np.ones((gray_img.shape[0], gray_img.shape[1]), dtype=np.uint8)
for i in range(new_img4.shape[0]):
    for j in range(new_img4.shape[1]):
        pix = gray_img[i][j] * a + b
        if pix > 255:
            new_img4[i][j] = 255
        elif pix < 0:
            new_img4[i][j] = 0
        else:
            new_img4[i][j] = pix

# a=-1, b=255, 图像翻转
new_img5 = 255 - gray_img

cv2.imshow('origin', imutils.resize(image, 400))
cv2.imshow('gray', imutils.resize(gray_img, 400))
cv2.imshow('a<0 and b=0', imutils.resize(new_img1, 400))
cv2.imshow('a>1 and b>=0', imutils.resize(new_img2, 400))
cv2.imshow('a<1 and b>=0', imutils.resize(new_img3, 400))
cv2.imshow('a=1 and b><0', imutils.resize(new_img4, 400))
cv2.imshow('a=-1 and b=255', imutils.resize(new_img5, 400))
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
