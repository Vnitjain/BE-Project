from utils import augument,load_image,preprocess
import cv2

import matplotlib.pyplot as plt

image = cv2.imread('test.jpg',flags=1)

norf = lambda x : x/127.5 -1
# # print(image)
# print(type(image))
# # image = image[:,:,::-1]
# image,str = augument(image,0.1)
# # print(image)
# print(type(image))
# image = cv2.flip(image,1)
# plt.interactive(True)
# plt.imshow(image)
# plt.show()

plt.imshow(image)

image = preprocess(image)
plt.imshow(image)
image = norf(image)
plt.imshow(image)
plt.show()