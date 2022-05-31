import numpy as np
import cv2


class Operation:

    def __init__(self):
        pass

    def merge(self, image_left, image_right, column):
        """
        Merge image_left and image_right at column (column)
        
        image_left: the input image 1
        image_right: the input image 2
        column: column at which the images should be merged

        returns the merged image at column
        """
        
        # add your code here

        width = image_left.shape[1]

        #create duplicate image and overlay right side after column
        merged_image = image_left.copy()
        for x in range(width):
            if x > column:
                merged_image[:,x] = image_right[:,x]

        # Please do not change the structure
        return merged_image  # Currently the original image is returned, please replace this with the merged image

    def intensity_scaling(self, input_image, column, alpha, beta):
        """
        Scale your image intensity.

        input_image: the input image
        column: image column at which left section ends
        alpha: left half scaling constant
        beta: right half scaling constant

        return: output_image
        """

        # add your code here

        width = input_image.shape[1]
        height = input_image.shape[0]

        scaled_image = input_image.copy()

        #iterate through properly so that it doesn't have so many page faults >.>
        #also scale acording to left alpha and right beta
        for y in range(height):
            for x in range(width):
                if x <= column:
                    scaled_image[y,x] = input_image[y,x]*alpha
                if x > column:
                    scaled_image[y,x] = input_image[y,x]*beta

        # Please do not change the structure
        return scaled_image  # Currently the input image is returned, please replace this with the intensity scaled image

    def centralize_pixel(self, input_image, column):
        """
        Centralize your pixels (do not use np.mean)

        input_image: the input image
        column: image column at which left section ends

        return: output_image
        """

        # add your code here

        width = input_image.shape[1]
        height = input_image.shape[0]
        sum_left = 0
        sum_right = 0
        left = 0
        right = 0

        centralized_image = input_image.copy()

        #calculate sum of intensities
        for y in range(height):
            for x in range(width):
                if x <= column:
                    sum_left += centralized_image[y,x]
                    left += 1
                if x > column:
                    sum_right += centralized_image[y,x]
                    right += 1

        #calculate average and offset
        average_left = sum_left/left
        average_right = sum_right/right
        offset_left = 128 - average_left
        offset_right = 128 - average_right

        #apply offset and account for clipping
        for y in range(height):
            for x in range(width):
                if x <= column:
                    temp = centralized_image[y,x] + offset_left
                    if temp < 0:
                        temp = 0
                    if temp > 255:
                        temp = 255
                    centralized_image[y,x] = temp
                if x > column:
                    temp = centralized_image[y,x] + offset_right
                    if temp < 0:
                        temp = 0
                    if temp > 255:
                        temp = 255
                    centralized_image[y,x] = temp

        return centralized_image   # Currently the input image is returned, please replace this with the centralized image
