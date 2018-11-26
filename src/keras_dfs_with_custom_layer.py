# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 16:59:42 2018

@author: Erik
"""

from keras import Sequential
from keras.layers import Dense
from OneToOne import OneToOne
from keras.regularizers import l2, l1, l1_l2
from keras.optimizers import SGD
import numpy as np
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.constraints import max_norm


'''
This is the main thing we're working with.  Increasing the regularization on the input layer with DECREASE the number of features
selected.  Setting it to 0 allows the neural network to just grab everything because it can.  We can definitely just increase this
until the quality of the model starts to erode.  Just before that point we will have a minimal feature set and a high quality model which
is what we are going for I think.
'''
FEATURE_REG =1 #discourage features from being selected

'''This is also necessary, otherwise the neural net could just ramp up the rest of the weights to compinsate for the
surpression on the input layer.
'''
MODEL_REG = 0.0001 #discourage complex model

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
#done one hot encoding===================


X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size = 0.2)
X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size = 0.5)



ffnn = Sequential()

# this model definitely will break if number of nodes and input shape differ.  They are one to one and I haven't figured out how to 
#   fully automate their connection
ffnn.add(OneToOne(102, name = 'input', input_shape = (102, ), use_bias = False, activation = 'linear', kernel_regularizer = l2(FEATURE_REG)))


ffnn.add(Dense(128, name = 'layer1', activation = 'sigmoid', kernel_regularizer = l1(MODEL_REG)))
ffnn.add(Dense(64, name = 'layer2', activation = 'sigmoid', kernel_regularizer = l1(MODEL_REG)))
ffnn.add(Dense(7, name = 'output', activation = 'softmax'))
ffnn.compile(optimizer = SGD(lr = 0.01),
              loss = 'categorical_crossentropy',
              metrics = ['accuracy'])

#really fast run of the model, just 15 epochs and 100 batch size.  We can improve with more epochs and smaller batch sizes
#but the model slows down then.
ffnn.fit(x = X_train, y = y_train, epochs = 100, batch_size = 100, validation_data = [X_val, y_val])

#get accuracy
print(ffnn.evaluate(X_test, y_test))

#retrieve feature weights
feature_weights = ffnn.get_layer('input').get_weights()[0]

#get the ones that exceed a certain threshold in magnitude
selected = abs(feature_weights) > 0.0001 #may need to figure out better threshold, study was using 1/1000 of max in the vector

#print weight and selection status
for i in range(20):
    print(feature_weights[i], end = "--")
    print(selected[i])

#report total number selected
print("Total features selected: " + str(sum(selected)))
