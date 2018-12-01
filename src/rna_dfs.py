# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 10:11:52 2018

@author: Erik
"""

from DFS import DFS
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

X = pd.read_csv('../data/rna/data.csv')
y_str = pd.read_csv('../data/rna/labels.csv')

#they come through with a string
X = X.drop('Unnamed: 0', axis = 1)
y_str = y_str.drop('Unnamed: 0', axis = 1)

#forgot about this little guy, get dummies one hot encodes from strings!
y = pd.get_dummies(y_str)

X = X.fillna(0)
X = (X - X.min()) / (X.max() - X.min())
X = X.fillna(0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)


lambdas = [0, 0.000001, 0.00005, 0.00001, 0.0001]
for lda in lambdas:
    model = DFS(in_dim = len(X_train.columns), 
                num_classes = len(y_train.columns),
                alpha1 = 0.00001, 
                lambda1 = lda,
                learning_rate = 0.5)
    
    model.fit(X_train, y_train, batch_size = 10, epochs = 50, validation_data = [X_test, y_test])
    model.write_features('../results/rna_featurs_' + str(lda) + ".csv", X_train.columns)
    model.write_predictions('../results/rna_predictions' + str(lda) + ".csv", X_test, y_test)