import pandas as pd
import numpy as np
import cv2

IMAGE_HEIGHT,IMAGE_WIDTH,CHANNELS = 70, 180, 3
IMAGE_DIM = (IMAGE_HEIGHT,IMAGE_WIDTH,CHANNELS)


def load_image(img_path,steering,datadir='data/'):
    r_index = np.random.randint(0,3)
    path = img_path[r_index]
    if r_index == 0:
        steering -= 0.2

    if r_index == 2:
        steering += 0.2

    return cv2.imread(datadir+str(path)),steering

def crop_image(image):
    return image[60:-25, :, :]

def resize_img(image):
    return cv2.resize(image, (IMAGE_WIDTH,IMAGE_HEIGHT), cv2.INTER_AREA)

def rgb2yuv(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2YUV)


def preprocess(image):
    image = crop_image(image)
    image = resize_img(image)
    image = rgb2yuv(image)
    return image

def flip_image(image,steering):

    steering *= -1
    return cv2.flip(image,1), steering

def augument(image,steering):

    image = preprocess(image)

    if np.random.randint(0,2):
        flip_image(image,steering)
    return image, steering




def batch_processing(X,Y,batch_size):
    images = np.zeros([batch_size,IMAGE_HEIGHT,IMAGE_WIDTH,CHANNELS])
    steering_angles = np.zeros(batch_size)

    print(images.shape)
    print(steering_angles.shape)

    while True:
        batch_iter = 0
        for index in np.random.permutation(X.shape[0]):
            image,steering = load_image(X[index],Y[index])
            images[batch_iter],steering_angles[batch_iter] = augument(image,steering)
            # print("IMG:{} ,{}".format(batch_iter, image[batch_iter].shape))
            batch_iter += 1

            if batch_iter == batch_size - 1:
                yield images,steering_angles
                break

