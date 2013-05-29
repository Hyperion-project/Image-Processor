from Tkinter import Image

__author__ = 'Maikel Hofman'

import numpy as np
import cv2

Image = cv2.imread("C:\Users\Maikel\Dropbox\Project 3D-Scanner\Research\Image processing\\2012-09-17 12.57.53.jpg")
imageDimension = Image.shape

# Do an inplace conversion to a float. The standard uint8 cannot be used because it has no room for
# negative numbers
Image = Image.astype(np.float, copy=False)

# Create an array with zeros that has the same (x, y) size of the picture but only 2 dimensions
zeroArray = np.zeros((imageDimension[0], imageDimension[1], 1))

# Remove the colors green and blue from the image
np.copyto(Image[:, :, 0:2], zeroArray, "safe")

# Create gaussian kernel and apply
gaussianImage = cv2.GaussianBlur(Image, (3, 3), 0.5)

# Apply threshold and remove negative numbers
gaussianImage[:, :, 2] -= 170
gaussianImage[:, :, gaussianImage < 0] = 1.0e-15

Coords = list()

# Run a loop through all the rows and find the maximum. Then use a gaussian approximation to find
# the sup-pixel offset.
# TODO: See if this part can be vectorized, should be faster

# Get image imagePlane
imagePlane = gaussianImage[:, :, 2]
for i in range(0, (imageDimension[0] - 1)):
    index = imagePlane[i, :].argmax()
    maxValue = imagePlane[i, index]

    if maxValue > 1.0e-15:
        part1 = np.log(imagePlane[i, index - 1]) - np.log(imagePlane[i, index + 1])
        part2 = np.log(imagePlane[i, index - 1]) - 2 * np.log(imagePlane[i, index]) + np.log(
            imagePlane[i, index + 1])
        delta = 0.5 * (part1/part2)
        Coords.append((i, index+delta))