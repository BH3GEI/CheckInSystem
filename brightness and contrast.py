import cv2
import numpy as np
import imutils

def c_and_b(arg):
    ''''''
    cnum = cv2.getTrackbarPos(trackbar_name1, wname)
    bnum = cv2.getTrackbarPos(trackbar_name2, wname)
    #print(bnum)
    cimg = np.ones((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            lst = 0.1*cnum*img[i, j] + bnum
            cimg[i, j] = [int(ele) if ele < 255 else 255 for ele in lst]
    cv2.imshow(wname, imutils.resize(cimg, 800))


wname = 'brightness and contrast'
trackbar_name1 = 'contrast'
trackbar_name2 = 'brightness'
img = cv2.imread('data/jm/1.jpg')
height, width = img.shape[:2]
img = cv2.resize(img, (int(width/height*400), 400), interpolation=cv2.INTER_CUBIC)

cv2.namedWindow(wname)
cv2.createTrackbar(trackbar_name1, wname, 10, 20, c_and_b)
cv2.createTrackbar(trackbar_name2, wname, 0, 100, c_and_b)

c_and_b(0)


if cv2.waitKey(0) == ord('A'):
    cv2.destroyAllWindows()

