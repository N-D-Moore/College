import numpy as np
import math
import cv2


class Filtering:

    def __init__(self, image, filter_name, filter_size, var = None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        global_var: noise variance to be used in the Local noise reduction filter
        S_max: Maximum allowed size of the window that is used in adaptive median filter
        """

        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filter_size = filter_size
        self.global_var = var
        self.S_max = 15

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""

        temp = 0
        for x in roi:
            temp = temp + x
        temp = temp/len(roi)

        #honestly want to just return sum(roi)/len(roi) but not sure if that is allowed in the assignment

        return temp

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""
        
        temp = 0
        for x in roi:
            if temp == 0:
                temp = x
            else:
                temp = temp * x
        temp = temp**(1/len(roi))

        return temp

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""

        # I am assuming this is variance squared? considering the formula for local noise has a square for local variance
        temp_var = 0
        temp_mean = self.get_arithmetic_mean(roi)
        for x in roi:
            temp_var = temp_var + ((x-temp_mean)**2)
        temp_var = temp_var/(len(roi)-1)

        #middle number will be the point
        temp = roi[int(len(roi)/2)]

        temp = temp - ((self.global_var/temp_var)*(temp - temp_mean))

        return temp

    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi"""

        #there is a formula for an even median but since all of these roi are odd i am not doing that ie 3x3 = 9, 5x5 = 25, etc.
        #also python has median built in but doing it this way since the directions said to use own computations
        #but also says i can use the median function so i am only using the sort function

        temp = roi
        temp.sort()
        #round down aka int due to indexes starting at 0
        median = temp[int(len(temp)/2)]

        return median


    def get_adaptive_median(self, roi):
        """Computes the harmonic filter
                        takes as input:
        kernel: a list/array of intensity values
        order: order paramter for the
        returns the harmonic mean value in the current kernel"""

        z_min = min(roi)
        z_max = max(roi)
        z_med = self.get_median(roi)
        z_xy = roi[int(len(roi)/2)]
        if len(roi) <= (self.S_max)*(self.S_max):
            A1 = z_med - z_min
            A2 = z_med - z_max
            if A1>0 and A2<0:
                B1 = z_xy - z_min
                B2 = z_xy - z_max
                if B1>0 and B2<0:
                    return z_xy
                else:
                    return z_med
            else:
                if len(roi) == (self.S_max)*(self.S_max):
                    return z_med
                else:
                    return -1
            asdf
        else:
            return z_med

        return 0

    def filtering(self):
        """performs filtering on an image containing gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernal and apply a mathematical
        operation for all the elements with in the kernel. For example, mean, median and etc.

        Steps:
        1. add the necesssary zero padding to the noisy image, that way we have sufficient values to perform the operati
        ons on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the ouput image.
        5. return the output image

        Note: You can create extra functions as needed. For example if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """
        #pad by max size due to adaptive median requiring increasing sizes (just makes it easier)
        pad = int(self.S_max/2)
        kernal = int(self.filter_size/2)

        width = np.shape(self.image)[0]
        height = np.shape(self.image)[1]

        padded_image = np.zeros((width+pad+pad,height+pad+pad))
        new_image = self.image.copy()

        for x in range(pad, width+pad):
            for y in range(pad, height+pad):
                padded_image[x][y] = self.image[x-pad][y-pad]

        for x in range(pad, width+pad):
            for y in range(pad, height+pad):
                temp_kernal = kernal
                roi = []
                for i in range(x-kernal,x+kernal+1):
                    for j in range(y-kernal,y+kernal+1):
                        roi.append(padded_image[i][j])
                temp = self.filter(roi)
                if temp == -1:
                    while temp == -1:
                        roi = []
                        temp_kernal = temp_kernal + 2
                        for i in range(x-temp_kernal,x+temp_kernal+1):
                            for j in range(y-temp_kernal,y+temp_kernal+1):
                                roi.append(padded_image[i][j])
                        temp = self.filter(roi)
                new_image[x-pad][y-pad] = temp

        return new_image

