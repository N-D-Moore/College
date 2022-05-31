from .interpolation import interpolation
import math, cv2
import numpy as np

class Geometric:
    def __init__(self):
        pass

    def forward_rotate(self, image, theta):
        """Computes the forward rotated image by and angle theta
                image: input image
                theta: angle to rotate the image by (in radians)
                return the rotated image"""

        height = image.shape[0]
        width = image.shape[1]
        rotated_height = round(height*math.cos(theta)+width*math.sin(theta))
        rotated_width = round(width*math.cos(theta)+height*math.sin(theta))
        #offset is just first origin x of new rotated image
        offset = round(256*math.sin(theta)+0*math.cos(theta))


        temp_image = np.zeros([rotated_height, rotated_width],dtype=np.uint8)

        for i in range(height):
            for j in range(width):
                #
                new_y = round(i*math.sin(theta)+j*math.cos(theta)) #offset by 0 aka nothing
                new_x = round(i*math.cos(theta)-j*math.sin(theta))+offset

                if 0 <= new_x and 0 <= new_y and new_x < rotated_width and new_y < rotated_height:
                    temp_image[new_x,new_y]=image[i,j]

        return temp_image

    def reverse_rotation(self, rotated_image, theta, origin, original_shape):
        """Computes the reverse rotated image by and angle theta
                rotated_image: the rotated image from previous step
                theta: angle to rotate the image by (in radians)
                Origin: origin of the original image with respect to the rotated image
                Original shape: Shape of the orginal image
                return the original image"""

        temp_image = np.zeros([original_shape[0], original_shape[1]],dtype=np.uint8)

        for i in range(rotated_image.shape[0]):
            for j in range(rotated_image.shape[1]):
                x = i - origin[0]
                y = j - origin[1]

                new_y = round(-x*math.sin(theta)+y*math.cos(theta))
                new_x = round(x*math.cos(theta)+y*math.sin(theta))

                if 0 <= new_x and 0 <= new_y and new_x < original_shape[0] and new_y < original_shape[1]:
                    temp_image[new_x,new_y]=rotated_image[i,j]

        return temp_image

    def rotate(self, image, theta, interpolation_type):
        """Computes the reverse rotated image by and angle theta
                image: the input image
                theta: angle to rotate the image by (in radians)
                interpolation_type: type of interpolation to use (nearest_neighbor, bilinear)
                return the original image"""

        height = image.shape[0]
        width = image.shape[1]
        rotated_height = round(height*math.cos(theta)+width*math.sin(theta))
        rotated_width = round(width*math.cos(theta)+height*math.sin(theta))
        #offset is just first origin x of new rotated image
        offset = round(256*math.sin(theta)+0*math.cos(theta))


        temp_image = np.zeros([rotated_height, rotated_width],dtype=np.uint8)

        for i in range(height):
            for j in range(width):
                #
                new_y = round(i*math.sin(theta)+j*math.cos(theta)) #offset by 0 aka nothing
                new_x = round(i*math.cos(theta)-j*math.sin(theta))+offset

                if 0 <= new_x and 0 <= new_y and new_x < rotated_width and new_y < rotated_height:
                    temp_image[new_x,new_y]=image[i,j]

        if interpolation_type == "nearest_neighbor":
            for i in range(rotated_height):
                for j in range(rotated_width):
                    x = i - offset
                    y = j

                    new_y = round(-x*math.sin(theta)+y*math.cos(theta))
                    new_x = round(x*math.cos(theta)+y*math.sin(theta))

                    if 0 <= new_x and 0 <= new_y and new_x < width and new_y < height:
                        if temp_image[i,j] == 0:
                            temp_image[i,j] = image[new_x,new_y]

            return temp_image

        if interpolation_type == "bilinear":
            for i in range(rotated_height):
                for j in range(rotated_width):
                    x = i - offset
                    y = j

                    new_y = round(-x*math.sin(theta)+y*math.cos(theta))
                    new_x = round(x*math.cos(theta)+y*math.sin(theta))

                    if 0 <= new_x and 0 <= new_y and new_x < width-1 and new_y < height-1:
                        if temp_image[i,j] == 0:
                            p1 = [new_x-1,new_y-1,image[new_x-1,new_y-1]]
                            p2 = [new_x+1,new_y-1,image[new_x+1,new_y-1]]
                            p3 = [new_x-1,new_y+1,image[new_x-1,new_y+1]]
                            p4 = [new_x+1,new_y+1,image[new_x+1,new_y+1]]
                            p5 = [new_x,new_y,temp_image[i,j]]
                            temp_image[i,j] = interpolation.bilinear_interpolation(self, p1,p2,p3,p4,p5)

            return temp_image

        return image


