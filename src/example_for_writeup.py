from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from OneToOne import OneToOne
from keras.optimizers import SGD
from keras.utils import to_categorical
import numpy as np 

X = np.array([[0,0],[0,10],[1,0],[1,10]])
y = np.array([[0],[1],[1],[0]])
y = to_categorical(y)

model = Sequential()
#model.add(OneToOne(2, input_dim = 2, use_bias = False))
model.add(Dense(2, input_dim = 2, activation = 'sigmoid'))
model.add(Dense(2, activation = 'softmax'))

sgd = SGD(lr=0.05)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

model.fit(X, y, batch_size=4, epochs = 10000)
print(model.predict(X))