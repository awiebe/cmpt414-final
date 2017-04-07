import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

print "reading", sys.argv[1]

def showSmall(image):
	small = cv2.resize(image, (0,0), fx=0.2, fy=0.2) 
	cv2.imshow('ImageWindow',small)
	cv2.waitKey()

img = cv2.imread(sys.argv[1])




# # Convert BGR to HSV
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# # define range of blue color in HSV [0,180],[0,255],[0,255]
# lower_blue = np.array([0,0,0])
# upper_blue = np.array([180,120,255])
# # Threshold the HSV image to get only blue colors
# mask = cv2.inRange(hsv, lower_blue, upper_blue)
# # Bitwise-AND mask and original image
# res = cv2.bitwise_and(img,img, mask= mask)

# showSmall(hsv)
# showSmall(mask)
# showSmall(res)

#plot hsv histogram  
# hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# hist = cv2.calcHist( [hsv], [0, 1], None, [180, 256], [0, 180, 0, 256] )

# plt.imshow(hist,interpolation = 'nearest')
# plt.show()

img = cv2.imread(sys.argv[1],0)
# global thresholding
ret1,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
# Otsu's thresholding
ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# Otsu's thresholding after Gaussian filtering
blur = cv2.GaussianBlur(img,(5,5),0)
ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

print "Wrote file Global Thresholding as: glbThreshold127.jpg"
cv2.imwrite("glbThreshold127.jpg",th1)

print "Wrote file Otsu Thresholding as: otsuThreshold.jpg"
cv2.imwrite("otsuThreshold.jpg",th3)

# plot all the images and their histograms
images = [img, 0, th1,
		  blur, 0, th3]
titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
		  'Original Noisy Image','Histogram',"Otsu's Thresholding",
		  'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]
for i in xrange(2):
	plt.subplot(2,3,i*3+1),plt.imshow(images[i*3],'gray')
	plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,i*3+2),plt.hist(images[i*3].ravel(),256)
	plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,i*3+3),plt.imshow(images[i*3+2],'gray')
	plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
	
print "showing"
plt.show()



# print "gaussian threshold"
# img = cv2.medianBlur(img,31)
# 
# window_size=5
# c=0
# 
# ret,th1 = cv2.threshold(img,100,255,cv2.THRESH_BINARY)
# th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
# 	   cv2.THRESH_BINARY,window_size,c)
# th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
# 		cv2.THRESH_BINARY,window_size,c)
# 
# titles = ['Original Image', 'Global Thresholding (v = 127)',
# 		'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
# images = [img, th1, th2, th3]
# 
# fig, ax = plt.subplots()
# for i in xrange(4):
# 	plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
# 	plt.title(titles[i])
# 	plt.xticks([]),plt.yticks([])
# 
# 
# #sliders
# 
# # axcolor = 'lightgoldenrodyellow'
# # axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
# # samp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=c)
# # 
# # def update(val):
# # 	s = samp.val
# # 	th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,window_size,c)
# # 
# # 	th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,window_size,c)
# # 	for i in xrange(4):
# # 		plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
# # 		plt.title(titles[i])
# # 		plt.xticks([]),plt.yticks([])
# # 	
# # 
# # 
# # samp.on_changed(update)
# 
# plt.show()
