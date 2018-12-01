# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 16:57:45 2018

@author: Erik
"""

from DFS import DFS
from keras.utils import to_categorical
import numpy as np

#de normalizing
X = np.array([[0, 0], [0, 10], [1, 0], [1, 10]])
y = np.array([0, 1, 1, 0])
y = to_categorical(y)

model = DFS(2, 2, hidden_layers = [200], learning_rate = 0.05, lambda1 = 0.001, lambda2 = 0.5, alpha1 = 0.01, alpha2 = 0.5)
model.fit(x = X, y = y, batch_size = 1, epochs = 5000)
print(model.predict(X))
model.show_bar_chart()