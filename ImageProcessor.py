__author__ = 'Maikel Hofman'

import numpy as np
import cv2


class ImageProcessor():
    def __init__(self):
        self.Threshold = 170
        self.GaussianSigma = 0.5

    def process(self, Image):
        """ Process image to find the laser line.

        Keyword arguments:
            Image -- 3 dimensional array off the picture

        Return:
            Array consisting of tuples with a x and a y coordinate of the laserline
        """
        imageDimension = Image.shape

        # Do an inplace conversion to a float. The standard uint8 cannot be used because it has no room for
        # negative numbers.
        Image = Image.astype(np.float, copy=False)

        # Create an array with zeros that has the same (x, y) size of the picture but only 2 dimensions
        zeroArray = np.zeros((imageDimension[0], imageDimension[1], 1))

        # Remove the colors green and blue from the image
        np.copyto(Image[:, :, 0:2], zeroArray, "safe")

        # Create gaussian kernel and apply
        gaussianImage = cv2.GaussianBlur(Image, (3, 3), self.GaussianSigma)

        # Apply threshold and remove negative numbers
        gaussianImage[:, :, 2] -= self.Threshold
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
                delta = 0.5 * (part1 / part2)
                Coords.append((i, index + delta))

        return Coords