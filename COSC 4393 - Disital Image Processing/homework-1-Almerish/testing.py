import math
from cv2 import cv2
import numpy as np

def transform_cord(pt, transform_matrix):
    return np.sum(transform_matrix * pt, axis=1)

def get_origin(input_shape, theta):
    transformation_matrix = np.array([[math.cos(theta), -math.sin(theta)],
                                      [math.sin(theta), math.cos(theta)]])

    corners = {"tl": np.array([0, 0]),
               "tr": np.array([0, input_shape[1]]),
               "bl": np.array([input_shape[0], 0]),
               "br": np.array([input_shape[0], input_shape[1]])}

    transformed_corners = dict()
    min_x, min_y = np.inf, np.inf
    for k in corners:

        transformed_corners[k] = transform_cord(corners[k], transformation_matrix)

        if transformed_corners[k][0] < min_x:
            min_x = transformed_corners[k][0]

        if transformed_corners[k][1] < min_y:
            min_y = transformed_corners[k][1]
    return -min_x, -min_y

def display_image(window_name, image):
    """A function to display image"""
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)

def display_image2(window_name, image):
    """A function to display image"""
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)

image = cv2.imread("cameraman.jpg", 0)

theta = .5

origin = get_origin(image.shape, theta)

print(round(origin[0]))

height = image.shape[0]
width = image.shape[1]
rotated_height = round(height*math.cos(theta)+width*math.sin(theta))
rotated_width = round(width*math.cos(theta)+height*math.sin(theta))
print(height, width, rotated_height, rotated_width)
offset = round(256*math.sin(theta)+0*math.cos(theta))
print(offset)

temp_image = np.zeros([rotated_height, rotated_width],dtype=np.uint8)
temp_image2 = np.zeros([height, width],dtype=np.uint8)
temp_image3 = np.zeros([rotated_height, rotated_width],dtype=np.uint8)
temp_image4 = np.zeros([height, width],dtype=np.uint8)

original_centre_height   = round(((image.shape[0]+1)/2)-1)    #with respect to the original image
original_centre_width    = round(((image.shape[1]+1)/2)-1)

new_centre_height= round(((rotated_height+1)/2)-1)        #with respect to the new image
new_centre_width= round(((rotated_width+1)/2)-1)

for i in range(height):
    for j in range(width):
        #co-ordinates of pixel with respect to the centre of original image
        # y=i x=j
        new_y = round(i*math.sin(theta)+j*math.cos(theta))
        new_x = round(i*math.cos(theta)-j*math.sin(theta))+offset

        if 0 <= new_x and 0 <= new_y and new_x < rotated_width and new_y < rotated_height:
            temp_image3[new_x,new_y]=image[i,j]

display_image("image", temp_image3)

for i in range(rotated_height):
    for j in range(rotated_width):
        x = i - origin[0]
        y = j - origin[1]

        new_y = round(-x*math.sin(theta)+y*math.cos(theta))
        new_x = round(x*math.cos(theta)+y*math.sin(theta))

        if 0 <= new_x and 0 <= new_y and new_x <= 255 and new_y <= 255:
            temp_image4[new_x,new_y]=temp_image3[i,j]
            
print(temp_image3[0,0])
display_image("image", temp_image4)

for i in range(rotated_height):
    for j in range(rotated_width):
        x = i - origin[0]
        y = j - origin[1]

        new_y = round(-x*math.sin(theta)+y*math.cos(theta))
        new_x = round(x*math.cos(theta)+y*math.sin(theta))

        if 0 <= new_x and 0 <= new_y and new_x < width and new_y < height:
            if temp_image3[i,j] == 0:
                if temp_image3[i,j-1] > temp_image3[i,j+1]:
                    Q1 = temp_image3[i,j]= temp_image3[i,j+1]+(1/2)*(temp_image3[i,j-1]-temp_image3[i,j+1])
                else:
                    Q1 = temp_image3[i,j]= temp_image3[i,j-1]+(1/2)*(temp_image3[i,j+1]-temp_image3[i,j-1])
                

display_image("image", temp_image3)