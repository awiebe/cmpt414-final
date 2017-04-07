import cv2
import numpy as np
import sys


#Adapted from http://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
img_rows, img_cols = img.shape
center = (img_cols/2,img_rows/2)
smoothedImg = cv2.medianBlur(img,3)
invertedImage = cv2.bitwise_not(smoothedImg)

thresholdedimageResults = cv2.threshold(invertedImage,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
coords = np.column_stack(np.where(thresholdedimageResults[1] > 0))
minAreaRectResults = cv2.minAreaRect(coords)
if minAreaRectResults[2]<-45:
	angleToRotate = -(minAreaRectResults[2]+90)
else:
	angleToRotate = -(minAreaRectResults[2])
rotationMatrix = cv2.getRotationMatrix2D(center,angleToRotate,1.0)
rotatedImage = cv2.warpAffine(thresholdedimageResults[1],rotationMatrix,(img_cols,img_rows))

cv2.imshow('image',rotatedImage)
cv2.waitKey(0)
cv2.destroyAllWindows()