#!/usr/bin/env python

import numpy as np
import cv2

from scipy import misc
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Read image from directory
img = mpimg.imread('image/upper.png')
# Print image size
print 'Original image size is:{}'
print img.shape


# Gray scale and compress
img_1 = img[:,:,0]
img_new_size = misc.imresize(img,0.10,'bilinear')
img_gray = cv2.cvtColor(img_new_size,cv2.COLOR_RGB2GRAY)
print "New image size is: "
print img_new_size.shape

# image binaryzaiton
ret,img_bi = cv2.threshold(img_gray,155,255,cv2.THRESH_BINARY)

# save image and data to directory
plt.savefig("image/binary_image.png")
np.save('map/binary_image',img_bi)

# visualization
plt.imshow(img_bi,'gray')
plt.show()

