# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 12:54:37 2018

@author: Erik
"""

from keras import Sequential
from keras.layers import Dense
from OneToOne import OneToOne
from keras.optimizers import SGD, Adam
from keras.regularizers import l1, l2
from ElasticNetRegularizer import ElasticNetRegularizer
import numpy as np
import matplotlib.pyplot as plt


class DFS(Sequential):
    '''
    num_classes - integer. if there are 6 classes, you would just enter 6
    hidden_layers - iterable.  If you want a 128 node hidden layer followed by a 64 node hidden layer, you would put [128, 64]
    in_shape - tuple.  Shape of the input.  If you have 100 features you would just put (100, )
    
    These are the regularization terms, set to the defaults from the study if nothing is specified.
    lambda1 - double. Penatly for selecting a lot of features
    lambda2 - double between 0 and 1.  Trade off between l2 regularization and l1 regularization for input layer only. 
        Defined as (1 - lambda2) l2_norm + lambda2 * l1_norm
    alpha1 - double. same as lambda1 but for the weights of the model excluding the input layer
    alpha2 = double between 0 and 1.  Same as lambda 2 but for trade off on the model side.
    learning_rate - double. used in stochastic gradient decent.  Controls step size.
    '''
    def __init__(self, 
                 in_dim, 
                 num_classes,
                 hidden_layers = [128, 64], 
                 lambda1 = 0.003,
                 lambda2 = 1,
                 alpha1 = 0.0001,
                 alpha2 = 0,
                 learning_rate = 0.01,
                 hidden_layer_activation = 'sigmoid',
                 output_layer_activation = 'softmax',
                 loss_function = 'categorical_crossentropy',
                 addl_metrics = ['accuracy']):
        
        
        
        super().__init__()
        
        
        self.add(
                OneToOne(in_dim, 
                         name = 'input', 
                         input_dim = in_dim, 
                         use_bias = False,
                         kernel_regularizer = ElasticNetRegularizer(lambda1, lambda2)
                         )
                )
        
        for i, num_nodes in enumerate(hidden_layers):
            self.add(
                    Dense(num_nodes, 
                          name = 'layer' + str(i), 
                          activation = hidden_layer_activation, 
                          kernel_regularizer = ElasticNetRegularizer(alpha1, alpha2)
                          )
                    
                    )
        self.add(Dense(num_classes, name = 'output', 
                       activation = output_layer_activation,
                       kernel_regularizer = ElasticNetRegularizer(alpha1, alpha2)
                       )
                    )
        
        
        self.compile(optimizer = SGD(lr = learning_rate),
              loss = loss_function,
              metrics = addl_metrics)

    def get_input_weights(self):
        wts = self.get_layer('input').get_weights()[0]
        return wts.reshape(len(wts)) #convert from column vector to row vector
    
    '''
    handles categorical and binary output.  So, y must be one hot encoded or already in 0/1 format
    '''
    def accuracy(self, X, y):
        pred = self.predict(X)
        
        #categorical case
        if len(y[0] > 1):
            #translate prediction
            pred = np.argmax(pred, axis = 1)
            y = np.argmax(y, axis = 1)
        
        #binary case
        else:
            pred = np.round(pred)
        
        return np.sum(pred == y) / len(y)
    
    def show_bar_chart(self):
        wts = self.get_input_weights() #get raw data from neural net
        wts = np.abs(wts)
        y_pos = np.arange(len(wts))
        plt.bar(y_pos, wts)
        plt.show()
        
    def get_weight_feature_tuples(self, features):
        weights = self.get_input_weights()
        weights = abs(weights)
        return list(zip(features, weights))
                
    
    def get_top_features(self, num_features, features):
        def get_weight(e):
            return e[1]
        weights_features = self.get_weight_feature_tuples(features)
        sorted_weights = sorted(weights_features, key = get_weight, reverse = True)
        return sorted_weights[0:num_features]
    
    def write_features(self, file_name, features):
        weights_features = self.get_weight_feature_tuples(features)
        file = open(file_name, 'w')
        file.write('feature,weight\n')
        for weight_feature in weights_features:
            file.write(str(weight_feature[0]) + "," + str(weight_feature[1]) + '\n')
        file.close()
    
    def write_predictions(self, file_name, X, y_true):
        file = open(file_name, 'w')
        y_pred = self.predict(X)
        y_pred = y_pred.reshape(len(y_pred)) #go from column vector to row vector
        y_true = np.array(y_true)
        file.write('y_true,y_pred\n')
        for i in range(len(y_pred)):
            file.write(str(y_true[i]) 
            + "," + str(y_pred[i]) 
            + "\n")
        file.close()
