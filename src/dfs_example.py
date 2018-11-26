# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 13:27:50 2018

@author: Erik
"""

from DFS import DFS
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical


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

model = DFS(in_shape = (102, ), num_classes = 7, lambda1 = 0.003) #
model.fit(x = X_train, y = y_train, epochs = 100, batch_size = 100, validation_data = [X_val, y_val])
print(model.accuracy(X_test, y_test))
model.show_bar_chart()
