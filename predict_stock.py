import numpy as np  
import matplotlib.pyplot as plt
from numpy.lib.type_check import real
import pandas as pd
#pd.core.is_list_like = pd.api.types.is_list_like
import pandas_datareader as web
import datetime as dt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

from tensorflow.compat.v1 import ConfigProto, InteractiveSession
import os

import tensorflow as tf

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
'''
os.environ["CUDA_VISIBLE_DEVICES"] = '0' #use GPU with ID=0
config = ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.5 # maximun alloc gpu50% of MEM
config.gpu_options.allow_growth = True #allocate dynamically
sess = tf.Session(config = config)
'''

print('GPU: ',tf.test.is_gpu_available())
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

def dataInitialize(dataInput):
    api_data = dataInput

def modelTrain(code):

    sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))

    #TODO: Load Data
    company = code

    start = dt.datetime(2012,1,1)
    end = dt.datetime(2020,1,1)

    data = web.DataReader(company, 'yahoo', start, end)
    #print(data)

    #TODO: prepare data
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))

    x_train, y_train = [], []
    prediction_days = 30

    for x in range(prediction_days,len(scaled_data)):
        x_train.append(scaled_data[x-prediction_days:x, 0])
        y_train.append(scaled_data[x, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    #TODO: Build Model
    #? model is a functon set

    #! 序貫模型市多個網路層的線性堆疊(so called, 一路走到黑)，把它想像成一個管道，一端輸入原始資料而另一端輸出預測結果。傳統上sequential中每層layer是和上一層相聯絡的
    model = Sequential()

    #! 通過.add方法一個個將layer (function)加入模型中
    '''
    Sequential的第一層需要接收引述來倔任資料型態、
    1.長短期記憶(LSTM,Long Short-Term Memory)是遞歸神經網路(RNN,Recurrent Neural Network)的其中一種
    [units]: 指定數量(神經元數量)
    [return_sequence]: 若為true則返回整個序列，否則僅返回輸出序列的最後一個值
    [input_shape]: 指定輸入之維度(dimension)，LSTM輸入必為三維資料(分別為batch,time steps,input data)。
    batch為訓練過程中一次輸入的資料筆數(x值)，time step為資料的時間維度(若股票要藉由前30天資料預測則time step為30)(y值)，input data為單獨一個時間的資料(z值)
    e.g. https://ithelp.ithome.com.tw/articles/10214405
    2.丟棄法(Dropout)是一個對抗過擬和(overfitting)的正則化法，在訓練時每一次的迭代(epoch)皆以一定的機率丟棄隱藏層神經元，輸入的數值(小數點)為丟棄神經元的百分比
    e.g. 此處為0.2即為丟棄20%的神經元
    3.全連接層(Dense)，用來對對上一層的神經元進行全部連接，實現特徵的非線性組合
    '''
    model.add(LSTM(units=200, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    #model.add(Dropout(0.25))
    model.add(LSTM(units=200, return_sequences=True))
    model.add(Dropout(0.25))
    model.add(LSTM(units=200))
    model.add(Dense(units=1)) #* Prediction of the next closing value

    #! compile training model
    '''
    1.optimizer: 優化器，此處使用Adam(Adaptive Moment Estimation)作為優化器，是Momentum+RMSprop的強化版
    最常見的優化演算法是經典的隨機梯度下降演算法(SGD)
    2.loss: 損失函式，此處使用均方誤差(MSE, mean squared error)
    '''
    model.compile(optimizer='adam', loss='mean_squared_error')

    #! 訓練模型一般使用fit函式
    '''
    .fit(輸入資料,標籤,batch_size,epochs)
    1.輸入資料: 若模型只有一個輸入，那麼x的型別是numpy array，若模型有多個輸入，那麼x的型別應當為list，list的元素是對應於各個輸入的numpy array
    2.標籤: numpy array，通常為y值(實際結果)
    3.batch_size: 批數，指定進行梯度下降時每個batch包含的樣本數，訓練時一個batch的樣本會被計算一次梯度下降，使目標函式優化一步
    4.epochs: 迭代，訓練終止時的epoch值，訓練將在到達該epoch值時停止，當沒有initial_epoch時，它就是訓練的總輪數
    '''
    model.fit(x_train, y_train, epochs=60, batch_size=32)

    #? Test the model accuracy on existing data

    #TODO: Load test data
    test_start = dt.datetime(2020,1,1)
    test_end = dt.datetime.now()

    test_data = web.DataReader(company, 'yahoo', test_start, test_end)
    actual_prices = test_data['Close'].values

    total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

    model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
    model_inputs = model_inputs.reshape(-1,1)
    model_inputs = scaler.transform(model_inputs)


    #TODO: make predictions on test data

    x_test = []

    for x in range(prediction_days, len(model_inputs)+1): # ! +1 will include the predicted next day's value in plot
        x_test.append(model_inputs[x-prediction_days:x, 0])

    x_test = np.array(x_test)
    print('x_test: \n',x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    print('x_test reshape: \n',x_test)

    predicted_prices = model.predict(x_test)
    predicted_prices = scaler.inverse_transform(predicted_prices)


    #TODO: plot the test prediction
    plt.plot(actual_prices, color='black', label=f'Actual {company} Price')
    plt.plot(predicted_prices, color='red', label=f'Predicted {company} Price')
    plt.title(f'{company} Share Price')
    plt.xlabel('Time')
    plt.ylabel(f'{company} Share Price')
    plt.legend()
    plt.show()

    return model,model_inputs,scaler,prediction_days,predicted_prices[-1],total_dataset[-1]

def model_predict(model,model_inputs,scaler,prediction_days,last_predictPrice,today_closing_price):
    #TODO: Predict next day
    real_data = [model_inputs[len(model_inputs) - prediction_days:len(model_inputs), 0]]
    real_data = np.array(real_data)
    #print('real_data: \n',real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))
    print('real_data reshape: \n',real_data)

    prediction = model.predict(real_data)
    prediction = scaler.inverse_transform(prediction)
    print('today\'s closed price:', today_closing_price)
    print('today\'s predicted closing price:', last_predictPrice)
    if prediction[0]<last_predictPrice:
        print('Predict tendency: Price go Lower')
    else:
        print('Predict tendency: Price go higher')
    print(f'Prediction of next day\'s closing value: {prediction}')


userIn = 1
model,model_inputs,scaler,prediction_days,last_predictPrice,today_closing_price = None,None,None,None,None,None
print(tf.__version__)
while(userIn!=-1):
    print('Chooseing:\n(1) Model Train\n(2) Model Predict\n(-1) Exit')
    userIn = int(input())
    if userIn == 1:
        stock_code = input()
        model,model_inputs,scaler,prediction_days,last_predictPrice,today_closing_price = modelTrain(stock_code)

    elif userIn == 2:
        model_predict(model,model_inputs,scaler,prediction_days,last_predictPrice,today_closing_price)
    else:
        print('Ending...')
        break