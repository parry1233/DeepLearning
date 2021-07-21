import numpy as np
from keras.datasets import imdb
from matplotlib import pyplot

#load dataset
(x_train,y_train), (x_test,y_test) = imdb.load_data()
x = np.concatenate((x_train,x_test), axis = 0)
y = np.concatenate((y_train,y_test), axis = 0)

print("Training data: ")
print(x.shape)
print(y.shape)

#print("Classes: ")
#print(np.unique(y))

print("Number of words: ")
print(len(np.unique(np.hstack(x))))

print("Review length: ")
result = [len(_x) for _x in x]
print("Mean %.2f words (%f)" % (np.mean(result), np.std(result)))

##plot review length
pyplot.boxplot(result)
pyplot.show()