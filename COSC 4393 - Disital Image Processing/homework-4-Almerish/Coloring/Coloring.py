import numpy as np
import cv2
import math
import random

class Coloring:


    def intensity_slicing(self, image, n_slices):
      #Convert greyscale image to color image using color slicing technique.
      #takes as input:
      #image: the grayscale input image
      #n_slices: number of slices

      #Steps:

      # 1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
      # 2. Randomly assign a color to each interval
      # 3. Create and output color image
      # 4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to

      random.seed('rgb')

      width = np.shape(image)[0]
      height = np.shape(image)[1]

      rgb_image = np.zeros([width, height, 3], dtype=np.uint8)

      slices_rgb = np.zeros([n_slices+1, 3], dtype=np.uint8)
      #rounding down for slice size
      slice_size = int(255/n_slices)

      for x in range(0, n_slices+1):
        for y in range(0, 3):
          #decided to keep balck and white to have more readable images instead of fully random
          #you can remove the if statements and it will be fully random
          if x == 0:
            slices_rgb[x][y] = 0
          elif x==n_slices:
            slices_rgb[x][y] = 255
          else:
            slices_rgb[x][y] = random.randrange(0, 255)

      for x in range(0, width):
        for y in range(0, height):
          #divide by slice size and that is my slices_rgb index
          temp_slice = int(image[x][y]/slice_size)
          for z in range(0, 3):
            rgb_image[x][y][z] = slices_rgb[temp_slice][z]

      #returns color image
      return rgb_image

    def color_transformation(self,image, n_slices, theta):
      #Convert greyscale image to color image using color transformation technique.
      #takes as input:
      #image:  grayscale input image
      #colors: color array containing RGB values

      #Steps:
      # 1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
      # 2. create red values for each slice using 255*sin(slice + theta[0])
      #    similarly create green and blue using 255*sin(slice + theta[1]), 255*sin(slice + theta[2])
      # 3. Create and output color image
      # 4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to

      width = np.shape(image)[0]
      height = np.shape(image)[1]

      rgb_image = np.zeros([width, height, 3], dtype=np.uint8)

      #rounding down for slice size
      slice_size = int(255/n_slices)

      for x in range(0, width):
        for y in range(0, height):
          #divide by slice size and that is my slices_rgb index
          temp_slice = int(image[x][y]/slice_size)
          temp_center = (temp_slice*slice_size) + (slice_size/2)
          for z in range(0, 3):
            if temp_slice == 0:
              rgb_image[x][y][z] = 0
            elif temp_slice == n_slices:
              rgb_image[x][y][z] = 255
            else:
              rgb_image[x][y][z] = 255*math.sin(temp_center + theta[z])

      #returns color image
      return rgb_image



        

