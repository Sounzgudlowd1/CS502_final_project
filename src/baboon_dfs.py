# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 17:18:16 2018

@author: Erik
"""

import pandas as pd
from DFS import DFS
from keras.utils import to_categorical
from os import listdir
from sklearn.model_selection import train_test_split

#get rid of correlated features
bad_cols =['LAT_mean', 'LAT_mean_n', 'LAT_std', 'LON_std', 'LON_mean', 'LON_mean_n', 'BABOON_NODE_n', 'speed_imputed', 'TIME_S_mean', 'ID_mean_n','ID_mean', 'TIME_mean', 'TIME_S_mean_n','TIME_mean_n', 'NEIGH', 'NEIGH_n']

data_dir = "../data/baboon/"

'''
data = None
for i, file in enumerate(listdir(data_dir)):
    if i != 9: #9 is a problem child, I have absolutely no idea why but it is. So, BYE FELICIA!
        print("importing file " + str(i))
        if data is None:
            data = pd.read_csv(data_dir + file)
        else:
            data = data.append(pd.read_csv(data_dir + file), sort = False)

for col in bad_cols:
    if col in data.columns:
        data = data.drop(col, axis = 1)

#get rid of labels with -2
data = data[data.LABEL_O_majority >= 0]


y = data['LABEL_O_majority']

print(set(y))
y = y.replace(4, 1)  #set running and walking to the same thing
y = y.replace(3, 2)  #set standing at rest and sitting to the same thing


#get class count, necessary for nueral network input


y = to_categorical(y)
print(len(data.columns))
label_cols = ['NEIGH_O_n','LABEL_O_majority_n', 'LABEL_F_values', 'LABEL_O_values', 'NEIGH_F_n','LABEL_F_majority_n', 'LABEL_O_majority', 'LABEL_F_majority']
for col in label_cols:
    data = data.drop(col, axis = 1) #get rid of labels





#now handle NaN's
data = data.fillna(0)
#do dataframe normalization to 0-1 range
X = (data - data.min())/(data.max() - data.min())
#NaN's can creep back if data.max() - data.min() = 0
X = X.fillna(0)

#do test train split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
num_classes = len(y[0])
input_dim = len(X.columns)
#actually do neural net training
'''
lambda1s = [1, 10]
models = []
for lmda in lambda1s:
    print("Training on lambda = " + str(lmda))
    model = DFS(input_dim, num_classes, hidden_layers = [1024, 256], lambda1 = lmda, alpha1 = 0.001, learning_rate = 0.01)
    model.fit(X_train, y_train, batch_size = 100, epochs = 5, validation_data = [X_test, y_test])
    models.append(model)
