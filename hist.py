import cv2
import imutils
import matplotlib.pyplot as plt

wiki_img = cv2.imread('data/jm/6.jpg')
wiki_gray = cv2.cvtColor(wiki_img, cv2.COLOR_BGR2GRAY)

#对图像进行均衡化处理，增强图像对比度
wiki_equ = cv2.equalizeHist(wiki_gray)

cv2.imshow('wiki_origin', imutils.resize(wiki_img, 800))
cv2.imshow('wiki_gray', imutils.resize(wiki_gray, 800))
cv2.imshow('wiki_equ', imutils.resize(wiki_equ, 800))

hist = cv2.calcHist([wiki_gray], [0], None, [256], [0, 256])
equ_hist = cv2.calcHist([wiki_equ], [0], None, [256], [0, 256])
fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1)
ax1.plot(hist)
ax2 = fig.add_subplot(1, 2, 2)
ax2.plot(equ_hist)
plt.show()


if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()

