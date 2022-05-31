# For this part of the assignment, You can use inbuilt functions to compute the fourier transform
# You are welcome to use fft that are available in numpy and opencv

import numpy as np
import cv2


class Filtering:

    def __init__(self, image):
        """initializes the variables frequency filtering on an input image
        takes as input:
        image: the input image
        """
        self.image = image
        self.mask = self.get_mask

    def get_mask(self, shape):
        """Computes a user-defined mask
        takes as input:
        shape: the shape of the mask to be generated
        rtype: a 2d numpy array with size of shape
        """
        mask = np.ones((shape[0], shape[1]))
        cv2.rectangle(mask, (276,222), (290,236), 0, -1)
        cv2.rectangle(mask, (222,276), (236,290), 0, -1)

        return mask

    def post_process_image(self, image):
        """Post processing to display DFTs and IDFTs
        takes as input:
        image: the image obtained from the inverse fourier transform
        return an image with full contrast stretch
        -----------------------------------------------------
        You can perform post processing as needed. For example,
        1. You can perfrom log compression
        2. You can perfrom a full contrast stretch (fsimage)
        3. You can take negative (255 - fsimage)
        4. etc.
        """
        processed_image = np.zeros(np.shape(image), dtype = np.uint8)
        B = np.amax(image)
        A = np.amin(image)
        K = 255

        for x in range(np.shape(image)[0]):
            for y in range(np.shape(image)[1]):
                processed_image[x][y] = int((K/(B-A))*(image[x][y]-A)+0.5)

        return processed_image

    def filter(self):
        """Performs frequency filtering on an input image
        returns a filtered image, magnitude of DFT, magnitude of filtered DFT
        ----------------------------------------------------------
        You are allowed to used inbuilt functions to compute fft
        There are packages available in numpy as well as in opencv
        Steps:
        1. Compute the fft of the image
        2. shift the fft to center the low frequencies
        3. get the mask (write your code in functions provided above) the functions can be called by self.filter(shape)
        4. filter the image frequency based on the mask (Convolution theorem)
        5. compute the inverse shift
        6. compute the inverse fourier transform
        7. compute the magnitude
        8. You will need to do post processing on the magnitude and depending on the algorithm (use post_process_image to write this code)
        Note: You do not have to do zero padding as discussed in class, the inbuilt functions takes care of that
        filtered image, magnitude of DFT, magnitude of filtered DFT: Make sure all images being returned have grey scale full contrast stretch and dtype=uint8
        """

        fft_image = np.fft.fft2(self.image)
        fft_image = np.fft.fftshift(fft_image)
        dft_image = np.log(abs(fft_image))
        dft_image = dft_image.astype(np.uint8)
        dft_image = self.post_process_image(dft_image)

        mask = self.get_mask(np.shape(fft_image))
        filterd_fft = mask*fft_image
        filterd_dft_image = np.log(abs(filterd_fft))
        filterd_dft_image = filterd_dft_image.astype(np.uint8)
        filterd_dft_image = self.post_process_image(filterd_dft_image)

        inverse_fft = np.fft.ifftshift(filterd_fft)
        inverse_fft = np.fft.ifft2(inverse_fft)
        final_image = self.post_process_image(inverse_fft)

        return [final_image, dft_image, filterd_dft_image]
