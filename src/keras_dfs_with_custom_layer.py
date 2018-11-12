# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 16:59:42 2018

@author: Erik
"""

from keras import Sequential
from keras.layers import Dense
from OneToOne import OneToOne
from keras.regularizers import l2, l1
from keras.optimizers import SGD
import numpy as np
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.constraints import max_norm

data_dir= 'C:/Working/UIC/Fall2018/CS502/CS502_final_project/DECRES/data/'

# Get data
filename=data_dir + "GM12878_200bp_Data.txt";
X = np.loadtxt(filename,delimiter='\t',dtype='float32')

filename=data_dir + "GM12878_200bp_Classes.txt";
y_str = np.loadtxt(filename,delimiter='\t',dtype=object)

#do one hot encoding=====================
#transform to int
le = LabelEncoder()
y_int = le.fit_transform(y_str)
#and transform to encoded
y_enc = to_categorical(y_int)
#y_enc = y_enc.reshape((len(y_enc), 1, len(y_enc[0])))
#done one hot encoding===================


X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size = 0.2)
X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size = 0.5)



ffnn = Sequential()

ffnn.add(OneToOne(102, name = 'input', input_shape = (102, ), use_bias = False, activation = 'linear'))
ffnn.add(Dense(128, name = 'layer1', input_shape = (102, ), activation = 'relu', kernel_regularizer = l1(0.0001)))
ffnn.add(Dense(64, name = 'layer2', activation = 'relu', kernel_regularizer = l1(0.0001)))
ffnn.add(Dense(7, name = 'output', activation = 'softmax'))
ffnn.compile(optimizer = SGD(lr = 0.01),
              loss = 'categorical_crossentropy',
              metrics = ['accuracy'])


ffnn.fit(x = X_train, y = y_train, epochs = 100, batch_size = 100, validation_data = [X_val, y_val])

print(ffnn.evaluate(X_test, y_test))
