__author__ = 'Maikel Hofman'

import numpy as np
import cv2

Image = cv2.imread("C:\Users\Maikel\Dropbox\Project 3D-Scanner\Research\Image processing\\2012-09-17 12.57.53.jpg")
imageDimension = Image.shape

# Create an array with zeros that has the same (x, y) size of the picture but only 2 dimensions
zeroArray = np.zeros((imageDimension[0], imageDimension[1], 1))

# Remove the colors green and blue from the image
# TODO: See if unsafe can be removed
np.copyto(Image[:, :, 0:2], zeroArray, "unsafe")

# Create gaussian kernel and apply
newImage = cv2.GaussianBlur(Image, (3, 3), 0.5)

cv2.imwrite("C:\Users\Maikel\Dropbox\Project 3D-Scanner\Research\Image processing\\test-python.jpg", Image)