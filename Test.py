__author__ = 'Maikel'

import numpy as np
import cv2
print ("Hello World")

im = cv2.imread("C:\Users\Maikel\Dropbox\Project 3D-Scanner\Research\Image processing\\2012-09-17 12.57.53.jpg")
x = im.shape

# Create an array with zeros that has the same (x, y) size of the picture but only 2 dimensions
zeroArray = np.zeros((x[0], x[1], 1))

# Remove the colors green and blue from the image
# TODO: See if unsafe can removed
np.copyto(im[:, :, 0:2], zeroArray, "unsafe")



cv2.imwrite("C:\Users\Maikel\Dropbox\Project 3D-Scanner\Research\Image processing\\test-python.jpg", im)