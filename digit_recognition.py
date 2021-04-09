import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Conv2D, MaxPool2D, Flatten
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist

def load_data(): #? categorical_crossentropy
    (x_train,y_train), (x_test,y_test) = mnist.load_data()
    number = 10000
    x_train = x_train[0:number]
    y_train = y_train[0:number]
    x_train = x_train.reshape(number,28*28)
    x_test = x_test.reshape(x_test.shape[0],28*28)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    #? convert class vector to binary class matrices
    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)
    x_train = x_train
    x_test = x_test
    x_test = np.random.normal(x_test)
    x_train = x_train / 255
    x_test = x_test / 255

    return (x_train,y_train), (x_test,y_test)


(x_train, y_train), (x_test, y_test) = load_data()

#? Define and add layers to model
model = Sequential()
model.add(Dense(input_dim = 28*28, units = 633, activation='sigmoid'))
model.add(Dense(units=666,activation='sigmoid'))
model.add(Dense(units=666,activation='sigmoid'))
model.add(Dense(units=10,activation='softmax')) #! softmax 可以將10維陣列值界定於0-1之間，且10維總和為1，可以用來表達為某數字的機率

#? set configuration
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

#? train model
model.fit(x_train,y_train,batch_size=100,epochs=30)

#? evaluate the accuracy of model
train_result = model.evaluate(x_train,y_train)
test_result = model.evaluate(x_test,y_test)
print('Train accuraccy: ',train_result[1])
print('Test accuraccy: ',test_result[1])