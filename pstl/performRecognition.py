# Import the modules
import cv2
import os
from os import path
import gzip
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np
import _pickle as cPickle



dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, "digits_cls.pkl")
if path.exists(file_path):
    print("File exists")
else:
    print("File not found, sorry")


# Load the classifier
clf = joblib.load(file_path)


# Read the input image 
file_path = os.path.join(os.path.dirname(__file__), 'photo_4.jpg')
if path.exists(file_path):
    print("File exists", file_path)
else:
    print("File not found, sorry")
im = cv2.imread(file_path, 0)
# create background image
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9))
bg = cv2.dilate(im, kernel)
bg = cv2.GaussianBlur(bg, (5,5), 1)
# subtract out background from source
src_no_bg = 255 - cv2.absdiff(im, bg)
im_gray = None
im_gray_blur = None
# Convert to grayscale and apply Gaussian filtering
#im_gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
height, width= im.shape[:2]
print(width, height)
#im_gray_blur = cv2.GaussianBlur(im_gray, (5, 5), 0)

# Threshold the image
#ret, im_th = cv2.threshold(im_gray_blur, 90, 255, cv2.THRESH_BINARY_INV)

# threshold
maxValue = 255
thresh = 127
ret, im_th = cv2.threshold(src_no_bg, thresh, maxValue, cv2.THRESH_BINARY_INV)

# Find contours in the image
_,ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



# Get rectangles contains each contour
rects = [cv2.boundingRect(ctr) for ctr in ctrs]
# For each rectangular region, calculate HOG features and predict
# the digit using Linear SVM.
for rect in rects:
    # Draw the rectangles
    cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3) 
    # Make the rectangular region around the digit
    leng = int(rect[3] * 1.6)
    pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
    pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
    roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
    print(roi.shape)
    h, w = roi.shape
    # Resize the image
    if h > 0 and w > 0:
        roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
        roi = cv2.dilate(roi, (3, 3))
        # Calculate the HOG features
        roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
        nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
        cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)

cv2.imshow("Resulting Image with Rectangular ROIs", im_th)
file_path = os.path.join(os.path.dirname(__file__), 'photo_4_result.jpg')
cv2.imwrite(file_path, im_th)
cv2.waitKey()