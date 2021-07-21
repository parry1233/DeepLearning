import numpy as np
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense

docs = ['well done',
    'good work',
    'great effort',
    'nice work',
    'excellent',
    'weak',
    'poor effort',
    'not good',
    'poor work',
    'could have done better'
    ]
labels = np.array([1,1,1,1,1,0,0,0,0,0])

vocab_size = 50
encoded_docs = [keras.preprocessing.text.one_hot(d,vocab_size) for d in docs]
#print(encoded_docs)

max_length = 0
for encode_doc in encoded_docs:
    if len(encode_doc)>max_length:
        max_length = len(encode_doc)
padded_docs = keras.preprocessing.sequence.pad_sequences(encoded_docs, maxlen=max_length, padding='post')
#print(padded_docs)

model = Sequential()
model.add(Embedding(vocab_size, 8, input_length=max_length))
model.add(Flatten())
model.add(Dense(1,activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#print(model.summary())

model.fit(padded_docs, labels, epochs = 50, verbose=0)
loss, accuracy = model.evaluate(padded_docs, labels, verbose=0)
print('Accuracy:',(accuracy*100))