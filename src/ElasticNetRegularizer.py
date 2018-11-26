# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 13:38:19 2018

@author: Erik
"""
from tensorflow.python.ops import math_ops

'''
This returns lambda1 * ((1-lambda2) / 2 * l1 + lambda2 * l2)
'''
class ElasticNetRegularizer:
    def __init__(self, lambda1, lambda2):
        self.lambda1 = lambda1
        self.l1 = (1 - lambda2) / 2
        self.l2 = lambda2
    
    def __call__(self, x):
        l1_regularization = math_ops.reduce_sum(self.l1 * math_ops.square(x))
        l2_regularization = math_ops.reduce_sum(self.l2 * math_ops.abs(x))
        return self.lambda1 * (l1_regularization + l2_regularization)