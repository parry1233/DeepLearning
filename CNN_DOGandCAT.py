import numpy as np
import pandas as pd
import os
import cv2 #pip install opencv-python
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, Dense, Flatten, Activation, Conv2D, MaxPooling2D

from PIL import Image, ImageDraw

trainData_Dir = 'KaggleData/train'
trainData_Path = os.path.join(trainData_Dir)

x=[]
y=[]
convert = lambda category : int(category=='dog')
def create_train_data(path):
    for p in os.listdir(path):
        category = p.split('.')[0]
        category = convert(category)
        img_array = cv2.imread(os.path.join(path,p),cv2.IMREAD_GRAYSCALE)
        new_img_array = cv2.resize(img_array,dsize=(80,80))

        x.append(new_img_array)
        y.append(category)
create_train_data(trainData_Path)
x = np.array(x).reshape(-1,80,80,1)
y = np.array(y)

#! normalize data
x = x/255.0


model = Sequential()
model.add(Conv2D(64,(3,3),activation='relu',input_shape=x.shape[1:]))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(128,(3,3),activation='relu',input_shape=x.shape[1:]))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(128,(3,3),activation='relu',input_shape=x.shape[1:]))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(64,activation='relu'))
#add a softmax layer with 10 output units
model.add(Dense(1,activation='sigmoid'))

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
model.fit(x,y,epochs=3,batch_size=32)

testData_Dir = 'KaggleData/test1'
testData_Path = os.path.join(testData_Dir)
x_test = []
id_line = []
def create_test_data(path):
    for p in os.listdir(path):
        id_line.append(p.split('.')[0])
        img_array = cv2.imread(os.path.join(path,p),cv2.IMREAD_GRAYSCALE)
        new_img_array = cv2.resize(img_array,dsize=(80,80))
        x_test.append(new_img_array)
create_test_data(testData_Path)
x_test = np.array(x_test).reshape(-1,80,80,1)
#! normalize
x_test = x_test/255.0

predictions = model.predict(x_test)
predict_value = [int(round(p[0])) for p in predictions]
df = pd.DataFrame({'id':id_line,'predict value':predict_value})
df.to_csv('prediction.csv',index = False)

sampleData_Dir = 'KaggleData/sample'
sampleData_Path = os.path.join(sampleData_Dir)
sample_test=[]
sample_id = []
def sample_output(path):
   for p in os.listdir(path):
        sample_id.append(p.split('.')[0])
        img_array = cv2.imread(os.path.join(path,p),cv2.IMREAD_GRAYSCALE)
        new_img_array = cv2.resize(img_array,dsize=(80,80))
        sample_test.append(new_img_array)
sample_output(sampleData_Path)
sample_test = np.array(sample_test).reshape(-1,80,80,1)
sample_test = sample_test / 255.0

samPredictions = model.predict(sample_test)
samPredict_value = [int(round(p[0])) for p in samPredictions]
#TODO: show predict image
def Check(value):
    if value == 1:
        return 'Dog'
    else:
        return 'Cat'
for i in range(len(sample_id)):
    print(sample_id[i])
    print(samPredict_value[i])
    filename = 'KaggleData/sample/'+str(sample_id[i])+'.jpg'
    print(filename)
    print(Check(samPredict_value[i]))

    img = Image.open(filename)
    draw = ImageDraw.Draw(img)
    draw.text((100,200),Check(samPredict_value[i]),(255,255,255),size = 1000)
    img.save(str(sample_id[i])+'.png')