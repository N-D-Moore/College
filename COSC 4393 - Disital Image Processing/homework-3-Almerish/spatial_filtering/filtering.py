import numpy as np


class Filtering:

    def __init__(self, image):
        self.image = image

    def get_gaussian_filter(self):
        """Initialzes and returns a 5X5 Gaussian filter
            Use the formula for a 2D gaussian to get the values for a 5X5 gaussian filter
        """

        tempMatrix = np.zeros((3,3))
        mask = np.zeros((5,5))

        #standard deviation
        sd=1

        #(1/(2*np.pi*(sd**2))*np.exp(-(((x**2)+(y**2))/(2*(sd**2))))
        #this 2d gausian formula makes the heighest point is the top left (0,0)
        #so rotating it around the 5x5 with the generated 3x3 (0,0) as the center of the 5x5

        for u in range(3):
            for v in range(3):
                tempMatrix[u][v] = (1/(2*np.pi*(sd**2))*np.exp(-(((u**2)+(v**2))/(2*(sd**2)))))

        mask[0][0] = mask[4][0] = mask[0][4] = mask[4][4] = tempMatrix[2][2]
        mask[0][1] = mask[4][1] = mask[0][3] = mask[4][3] = tempMatrix[2][1]
        mask[1][0] = mask[3][0] = mask[3][4] = mask[1][4] = tempMatrix[1][2]
        mask[0][2] = mask[2][0] = mask[2][4] = mask[4][2] = tempMatrix[2][0]
        mask[1][1] = mask[3][1] = mask[1][3] = mask[3][3] = tempMatrix[1][1]
        mask[1][2] = mask[3][2] = tempMatrix[1][0]
        mask[2][1] = mask[2][3] = tempMatrix[0][1]
        mask[2][2] = tempMatrix[0][0]

        return mask

    def get_laplacian_filter(self):
        """Initialzes and returns a 3X3 Laplacian filter"""

        tempMatrix = np.zeros((3,3))

        #using Laplacian filter given in notes
        tempMatrix[0][0] = tempMatrix[0][2] = tempMatrix[2][0] = tempMatrix[2][2] = 0
        tempMatrix[0][1] = tempMatrix[1][0] = tempMatrix[2][1] = tempMatrix[1][2] = 1
        tempMatrix[1][1] = -4

        return tempMatrix

    def filter(self, filter_name):
        """Perform filtering on the image using the specified filter, and returns a filtered image
            takes as input:
            filter_name: a string, specifying the type of filter to use ["gaussian", laplacian"]
            return type: a 2d numpy array
                """

        #gaussian
        if filter_name == "gaussian":
            shape = np.shape(self.image)
            padded_array = np.zeros((shape[0]+4+4,shape[1]+4+4))
            new_image = np.zeros((shape[0]+2+2,shape[1]+2+2))
            mask = self.get_gaussian_filter()

            for x in range(4, np.shape(padded_array)[0]-4):
                for y in range(4, np.shape(padded_array)[1]-4):
                    padded_array[x][y] = self.image[x-4][y-4]

            normalization = 0
            for x in range(np.shape(mask)[0]):
                for y in range(np.shape(mask)[1]):
                    normalization += mask[x][y]
            normalization = 1/normalization

            for x in range(2, np.shape(padded_array)[0]-4):
                for y in range(2, np.shape(padded_array)[1]-4):
                    temp_sum = 0
                    #I didn't rotate the mask/kernel due to it being rotated 180 is the exact same do to it being symetrical
                    temp_sum = (mask[0][0]*padded_array[x-2][y-2]) + (mask[0][1]*padded_array[x-2][y-1]) + (mask[0][2]*padded_array[x-2][y]) + \
                        (mask[0][3]*padded_array[x-2][y+1]) + (mask[0][4]*padded_array[x-2][y+2])
                    temp_sum += (mask[1][0]*padded_array[x-1][y-2]) + (mask[1][1]*padded_array[x-1][y-1]) + (mask[1][2]*padded_array[x-1][y]) + \
                        (mask[1][3]*padded_array[x-1][y+1]) + (mask[1][4]*padded_array[x-1][y+2])
                    temp_sum += (mask[2][0]*padded_array[x][y-2]) + (mask[2][1]*padded_array[x][y-1]) + (mask[2][2]*padded_array[x][y]) + \
                        (mask[2][3]*padded_array[x][y+1]) + (mask[2][4]*padded_array[x][y+2])
                    temp_sum += (mask[3][0]*padded_array[x+1][y-2]) + (mask[3][1]*padded_array[x+1][y-1]) + (mask[3][2]*padded_array[x+1][y]) + \
                        (mask[3][3]*padded_array[x+1][y+1]) + (mask[3][4]*padded_array[x+1][y+2])
                    temp_sum += (mask[4][0]*padded_array[x+2][y-2]) + (mask[4][1]*padded_array[x+2][y-1]) + (mask[4][2]*padded_array[x+2][y]) + \
                        (mask[4][3]*padded_array[x+2][y+1]) + (mask[4][4]*padded_array[x+2][y+2])
                    temp_sum = temp_sum/normalization
                    new_image[x-2][y-2] = temp_sum

        #laplacian
        if filter_name == "laplacian":
            shape = np.shape(self.image)
            padded_array = np.zeros((shape[0]+1+1,shape[1]+1+1))
            new_image = np.zeros((shape[0],shape[1]))
            mask = self.get_laplacian_filter()

            for x in range(1, np.shape(padded_array)[0]-1):
                for y in range(1, np.shape(padded_array)[1]-1):
                    padded_array[x][y] = self.image[x-1][y-1]

            for x in range(1, np.shape(padded_array)[0]-1):
                for y in range(1, np.shape(padded_array)[1]-1):
                    #I didn't rotate the mask/kernel due to it being rotated 180 is the exact same do to it being symetrical
                    temp_sum = 0
                    temp_sum += (mask[0][0]*padded_array[x-1][y-1]) + (mask[0][1]*padded_array[x-1][y]) + (mask[0][2]*padded_array[x-1][y+1])
                    temp_sum += (mask[1][0]*padded_array[x][y-1]) + (mask[1][1]*padded_array[x][y]) + (mask[1][2]*padded_array[x][y+1])
                    temp_sum += (mask[2][0]*padded_array[x+1][y-1]) + (mask[2][1]*padded_array[x+1][y]) + (mask[2][2]*padded_array[x+1][y+1])
                    new_image[x-1][y-1] = temp_sum

        return new_image

