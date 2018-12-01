"""
Created on Sat Nov 11 12:10:41 2017

@author: Erik
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def columns_and_types(iData):
    out_list = []
    for x, y in zip(iData.columns, iData.dtypes):
        out_list.append((x, y))
    return out_list
    
def describe(iData, feature):
    #stats about sale price
    print(iData[feature].describe())
    print('Skew:')
    print(iData[feature].skew())
    print('Kurtosis:')
    print(iData[feature].kurtosis())
    print('End of sales summary statistics==========================\n\n')
    
    
def pair_plot(iData):
    cols = ['SalePrice','OverallQual','GrLivArea','GarageArea','1stFlrSF','FullBath','YearBuilt']
    sns.pairplot(iData[cols],size=2.5)
    plt.show()
    

    
def missing_data(iData):
    #missing data
    total = iData.isnull().sum().sort_values(ascending=False)
    percent = (iData.isnull().sum()/iData.isnull().count()).sort_values(ascending=False)
    dtype = iData.dtypes
    missing_data = pd.concat([total, percent, dtype], axis=1, keys=['Total', 'Percent', 'DataType'], sort = True)
    missing_data = missing_data.sort_values( by = ['Total'], ascending = False)
    return missing_data

def feature_stats(iData, feature):
    print(feature, end = ' ')
    print(' with mean of 0 and standard deviation of 1==')
    feature_scaled = StandardScaler().fit_transform(iData[feature][:,np.newaxis]);
    low_range = feature_scaled[feature_scaled[:,0].argsort()][:10]
    high_range= feature_scaled[feature_scaled[:,0].argsort()][-10:]
    print('outer range (low) of the distribution:')
    print(low_range)
    print('\nouter range (high) of the distribution:')
    print(high_range)

def top_k_correlations(iData, k):
    corrmat = iData.corr()
    cols = corrmat.nlargest(k,'SalePrice')['SalePrice'].index
    cm = np.corrcoef(iData[cols].values.T)
    sns.set(font_scale=1.25)
    sns.heatmap(cm,cbar=True,annot=True,square=True,fmt='.2f',annot_kws={'size':10},yticklabels=cols.values,xticklabels=cols.values)
    plt.show()
    
def all_correlations(iData):
    corrmat = iData.corr()
    f, ax = plt.subplots(figsize=(12,9))
    sns.heatmap(corrmat, vmax = 0.8, square =True)
    plt.show()
    
def histogram(iData, feature):
    sns.distplot(iData[feature], fit= stats.norm);
    fig = plt.figure()
    res = stats.probplot(iData[feature], plot=plt)
    plt.show()
    

def box_whisker_plot(iData, feature1, feature2):
    data = pd.concat([iData[feature1], iData[feature2]], axis=1)
    f, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x=feature1, y=feature2, data=data);
    plt.show()
    
    
def scatter_plot(iData, feature1, feature2):
    data = pd.concat([iData[feature1], iData[feature2]], axis=1)
    data.plot.scatter(x=feature1, y=feature2);
    plt.show()
    
def scatter_plot_nonzero(iData, feature1, feature2):
    iData = iData.loc[iData[feature1] > 0] 
    data = pd.concat([iData[feature1], iData[feature2]], axis=1)
    data.plot.scatter(x=feature1, y=feature2);
    plt.show()

def pred_vs_actual_plot(prediction, actual):
    """
    Scatter plot of prediction vs actual with line on identity

    :param prediction: predicted values, array-like
    :param actual: actual values, array-like
    """
    plt.figure(figsize=(7, 7))

    plt.scatter(actual, prediction, s=20)
    plt.plot([min(actual), max(actual)], [min(actual), max(actual)])

    plt.title('Predicted vs. Actual')
    plt.xlabel('Actual Sale Price')
    plt.ylabel('Predicted Sale Price')
    plt.show()
