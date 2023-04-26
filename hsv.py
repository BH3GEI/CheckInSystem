import cv2
import imutils
import numpy as np


def s_and_b(arg):
    lsImg = np.zeros(image.shape, np.float32)
    hlsCopy = np.copy(hlsImg)

    l = cv2.getTrackbarPos('l', 'l and s')
    s = cv2.getTrackbarPos('s', 'l and s')
    # 1.调整亮度饱和度(线性变换)、 2.将hlsCopy[:,:,1]和hlsCopy[:,:,2]中大于1的全部截取
    hlsCopy[:, :, 1] = (1.0 + l / float(MAX_VALUE)) * hlsCopy[:, :, 1]
    hlsCopy[:, :, 1][hlsCopy[:, :, 1] > 1] = 1
    # HLS空间通道2是饱和度，对饱和度进行线性变换，且最大值在255以内，这一归一化了，所以应在1以内
    hlsCopy[:, :, 2] = (1.0 + s / float(MAX_VALUE)) * hlsCopy[:, :, 2]
    hlsCopy[:, :, 2][hlsCopy[:, :, 2] > 1] = 1
    # HLS2BGR
    lsImg = cv2.cvtColor(hlsCopy, cv2.COLOR_HLS2BGR)
    # 显示调整后的效果
    cv2.imshow("l and s", imutils.resize(lsImg, 650))


image = cv2.imread('data/jm/1.jpg', 1)
# 图像归一化，且转换为浮点型, 颜色空间转换 BGR转为HLS
fImg = image.astype(np.float32)
fImg = fImg / 255.0
# HLS空间，三个通道分别是: Hue色相、lightness亮度、saturation饱和度
# 通道0是色相、通道1是亮度、通道2是饱和度
hlsImg = cv2.cvtColor(fImg, cv2.COLOR_BGR2HLS)

l, s, MAX_VALUE = 100, 100, 100
cv2.namedWindow("l and s", cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar("l", "l and s", l, MAX_VALUE, s_and_b)
cv2.createTrackbar("s", "l and s", s, MAX_VALUE, s_and_b)

s_and_b(0)
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
