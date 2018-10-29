# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 18:32:35 2018

@author: Erik
"""
#pandas dataframes make csv reading really easy.
import pandas as pd
#types of layers and the function to convert to categorical
from keras.models import Sequential
from keras.layers import Dense, Activation, Input, LocallyConnected1D
from keras.utils import to_categorical
from keras.regularizers import l2, l1
import keras
import numpy as np
np.random.seed(8)
#used to split data
from sklearn.model_selection import train_test_split

#get data
data = pd.read_csv('iris.csv')
print(data.columns)
#get only the left two columns
X_data = data.drop(['type'], axis = 1)
#get only the label column, type
y_data = data[['type']]

#transfer from 1, 2, 3 to [0,1,0,0], [0, 0, 1, 0], and [0,0,0,1] respectively
y_data = to_categorical(y_data)

#split into test and train, 30% test, 70% train
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size = 0.3, random_state = 8)

#no need validation set and test set, can't train network on data it will predict on
#this is seriously manditory.  If you use the test set direclty for validation then you are training on the test set!
X_validation, X_test, y_validation, y_test = train_test_split(X_test, y_test, test_size = 0.5, random_state = 8)

#type of neural network is sequential
model = Sequential()
#l1 regularized
model.add(Dense(4, input_shape = (3, ), activation = 'softmax', name = 'dense_one', kernel_regularizer = l1(0.2)))

#generate the model
model.compile(optimizer = keras.optimizers.SGD(lr = 0.1),
              loss = 'categorical_crossentropy',
              metrics = ['accuracy'],
              )

#actually do training
history = model.fit(x = X_train, y = y_train, epochs = 100, batch_size = 50, 
          validation_data = [X_validation, y_validation])



#now report accuracy with train and totally withheld test set
print("Train accuracy: ")
print(model.evaluate(X_train, y_train)[1]) #returns both loss and accuracy, so this is getting the accuracy

print("Test accuracy: ")
print(model.evaluate(X_test, y_test)[1]) #returns both loss and accuracy, so this is getting the accuracy

#the weights of the model with regularization.  So close!  Just need that one-to-one layer
print("\nWeights:")
print(model.get_layer('dense_one').get_weights())

#


