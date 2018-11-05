import numpy as np
import pandas as pd
import cv2
from os import listdir
from os.path import isfile, join
#import matplotlib.pyplot as plt
from keras.models import Model
from keras.models import Sequential
from keras.layers import Input, UpSampling2D
from keras.layers import merge
from keras import backend as K
from keras.layers import Lambda, Concatenate
import argparse
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation,Conv2D,MaxPooling2D,Flatten,Dropout, InputLayer, Reshape
from keras.optimizers import Adam, Adadelta
from numpy import array
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import random
from tensorflow.python.lib.io import file_io
from io import StringIO
from PIL import Image
from keras.models import load_model, Model
import io
import os
import shutil


def IOU_calc(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)

    return 2*(intersection+2) / (K.sum(y_true_f) + K.sum(y_pred_f) +2)

def IOU_calc_loss(y_true, y_pred):
    return -IOU_calc(y_true, y_pred)


def get_data(imgtype):
    train_images=[]
    path="~/Documents/Class/"
    for x in range(1,2):
        path="./Class"+str(x)+"/"
        #prina(path)
        read_file = file_io.read_file_to_string(path+imgtype+"/Label/Labels.txt")
        read_file = str(read_file)
        df = pd.read_fwf(path+imgtype+"/Label/Labels.txt")
        for i in range(0, len(df)):
           if(int(df.iloc[i][1])==1):
               fname=path+imgtype+"/"+str(df.iloc[i][2])
               print(fname)
               img=cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
               img=cv2.Canny(img, 100, 200)
               img=cv2.resize(img,(512,512))
               train_images.append([np.array(img)])
    return train_images



def predict_one2():
    #image_batch, mask_batch = next(validation_generator)
    #model = keras_model(img_width=512, img_height=512)
    model = load_model('loc1.h5',custom_objects={'IOU_calc_loss': IOU_calc_loss, 'IOU_calc': IOU_calc})
    #plot_model(model, to_file='model.png')
    fname="0595.PNG"
    img=cv2.imread(fname,0)
    img=cv2.Canny(img, 100, 200)
    cv2.imwrite("test12.jpg",img)
    #print(img.shape)
    #print(predicted_mask_batch.shape)
    #print(img.shape)
    #img =img.resize(img, (512,512))
    #img = np.array(img)
    #img =img.resize(img, (512,512))
    testimg=get_data("Test")
    X_train=get_data("Test")
    X_train_data = np.array([i[0] for i in X_train]).reshape(-1,512,512,1)
    #print(X_train_data.shape)
    predicted_mask_batch = model.predict(X_train_data)
    predicted_mask_batch = predicted_mask_batch*255
    #print(predicted_mask_batch[0,:,:,0])

    #predicted_mask_batch = predicted_mask_batch.reshape(512,512)

    #predicted_mask_batch = np.array(predicted_mask_batch)
    cv2.imwrite("./test1.jpg", predicted_mask_batch[0])
    img3=cv2.imread(fname,0)
    #image = image_batch[0]
    #predicted_mask = predicted_mask_batch[0].reshape(SIZE)
    #plt.imshow(img)
    #plt.imshow(predicted_mask_batch, alpha=0.6)




np.set_printoptions(threshold=np.inf, precision=8, floatmode='maxprec')
predict_one2()


