# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 18:32:35 2018

@author: Erik
"""
#pandas dataframes make csv reading really easy.
import pandas as pd
#types of layers and the function to convert to categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import keras
#used to split data
from sklearn.model_selection import train_test_split

#get data
data = pd.read_csv('iris.csv')
#get only the left two columns
X_data = data.iloc[:, :2]
#get only the label column, type
y_data = data[['type']]

#transfer from 1, 2, 3 to [0,1,0,0], [0, 0, 1, 0], and [0,0,0,1] respectively
y_data = to_categorical(y_data)

#split into test and train, 30% test, 70% train
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size = 0.3)

#no need validation set and test set, can't train network on data it will predict on
#this is seriously manditory.  If you use the test set direclty for validation then you are training on the test set!
X_validation, X_test, y_validation, y_test = train_test_split(X_test, y_test, test_size = 0.5)

#type of neural network is sequential, I'd have to consult Keras documents to give any  more detail
model = Sequential()

#add a single layer with 10 nodes.  There are two input parameters, so input dim = 2
#relu is the standard ramp function used in neural nets the shape is like ___/
    #essentailly max(0, x)
model.add(Dense(10, input_dim = 2, activation = 'relu'))
#add a second hidden layer, usually fewer and fewer nodes per hidden layer, this is such a small example it's way overdone
model.add(Dense(5, activation = 'relu'))
#softmax used in output layer, output layer must match number or categories, for whatever reason we are using 0, 1, 2 and 3
model.add(Dense(4, activation = 'softmax'))
#generate the model
model.compile(optimizer = keras.optimizers.SGD(lr = 0.01),
              loss = 'categorical_crossentropy',
              metrics = ['accuracy'])

#actually do training
history = model.fit(x = X_train, y = y_train, epochs = 1000, batch_size = 50, 
          validation_data = [X_validation, y_validation])

#now report accuracy with train and totally withheld test set
print("Train accuracy: ")
print(model.evaluate(X_train, y_train)[1]) #returns both loss and accuracy, so this is getting the accuracy

print("Test accuracy: ")
print(model.evaluate(X_test, y_test)[1]) #returns both loss and accuracy, so this is getting the accuracy


