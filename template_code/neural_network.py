# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 09:35:35 2018

@author: Erik
"""

import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def train_input_fn(features, labels, batch_size):
    """An input function for training"""
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)

    # Return the read end of the pipeline.
    return dataset.make_one_shot_iterator().get_next()

def eval_input_fn(features, labels, batch_size):
    """An input function for evaluation or prediction"""
    features=dict(features)
    if labels is None:
        # No labels, use only features.
        inputs = features
    else:
        inputs = (features, labels)

    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    # Batch the examples
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)

    # Return the read end of the pipeline.
    return dataset.make_one_shot_iterator().get_next()

CSV_COLUMN_NAMES = ['len', 'width', 'type']

print(tf.__version__)

data = pd.read_csv('iris.csv', names=CSV_COLUMN_NAMES, header=0)
X_data = data.iloc[:, :2]
y_data = data[['type']]
print(type(X_data))

X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size = 0.2)

feature_cols = []
for col in X_train.keys():
    feature_cols.append(tf.feature_column.numeric_column(key=col))

classifier = tf.estimator.DNNClassifier(feature_columns = feature_cols, hidden_units = [10, 10], n_classes = 2)

classifier.train(input_fn = lambda:train_input_fn(X_train, y_train, 100)
                , steps = 1000)

eval_result = classifier.evaluate(
        input_fn=lambda:eval_input_fn(X_test, y_test, 100))

print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

