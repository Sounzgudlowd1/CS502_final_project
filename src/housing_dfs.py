# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 13:08:00 2018

@author: Erik
"""
import pandas as pd
import housing_normalize as hn
import housing_outliers as ho
from DFS import DFS
from sklearn.model_selection import train_test_split

data = pd.read_csv('../data/housing/data.csv')

data = hn.fill_in_missing_values(data)
data = ho.remove_outliers(data)
data = hn.normalize(data)
X = data.drop('log_SalePrice', 1)
y = data['log_SalePrice']

X = (X - X.min()) / (X.max() - X.min())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)


# custom R2-score metrics for keras backend
from keras import backend as K

def r2_keras(y_true, y_pred):
    SS_res =  K.sum(K.square(y_true - y_pred)) 
    SS_tot = K.sum(K.square(y_true - K.mean(y_true))) 
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )

lambdas = [0, 0.0001, 0.001, 0.01, 0.1]
models = []
for lda in lambdas:
    reg_model = DFS(in_dim = len(X_train.columns), 
                    num_classes = 1, 
                    lambda1 = lda, 
                    alpha1 = 0.0001,
                    hidden_layers = [128, 32],
                    hidden_layer_activation = 'relu', 
                    output_layer_activation = 'linear', 
                    loss_function = 'mean_squared_error', 
                    learning_rate = 0.005,
                    addl_metrics = [r2_keras])
    
    reg_model.fit(x = X_train, y = y_train, batch_size = 10, epochs = 100, validation_data = [X_test, y_test])
    reg_model.write_features('../results/housing_weights_'+ str(lda) + '.csv', X.columns)
    reg_model.write_predictions('../results/housing_predictions_' + str(lda) + '.csv', X_test, y_test)
    

