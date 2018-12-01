# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 11:59:59 2017

@author: Erik
"""

import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from scipy.stats import skew


def remove_outliers(iData):
   
    iData = iData.drop(iData[iData['GrLivArea'] >4000].index)
    
    #based on lot frontage, anything with value > 300 removed
    iData = iData.drop(iData[iData['LotFrontage'] > 300].index)
    
    #based on lot area, anything with value > 100,000 removed
    iData = iData.drop(iData[iData['LotArea'] >30000].index)
    
    #based on sale price, anything with a value over 600,000
    iData = iData.drop(iData[iData['SalePrice'] > 600000].index)
    		
    iData = iData.drop(iData[iData['SalePrice'] < 40000].index)
    
    iData = iData.drop(iData[iData['WoodDeckSF'] > 800].index)
    
    return iData

#Generic Outlier detector method
#https://stackoverflow.com/questions/22354094/pythonic-way-of-detecting-outliers-in-one-dimensional-observation-data/22357811#22357811
def is_outlier(iData,iThresholdValue=3.5):
	if len(iData.shape) == 1:
		iData = iData[:,None]

	median = np.median(iData,axis=0)
	diff = np.sum((iData - median)**2,axis=-1)
	diff = np.sqrt(diff)
	med_abs_deviation = np.median(diff)

	modified_z_score = 0.6745 * diff/med_abs_deviation

	return modified_z_score > iThresholdValue

'''
	Outlier removal rules for continuous Data- 
	1. if missing data is more than 50 for a column = Drop the column
	2. if missing data is less than 50 for a column = Fill the column with median of data
	3. Remove any outlier with mean absolute deviation
	4. Find skewness, if any variable is skewed more than 75% then log transform the variable
	5. Normalize the data between 1 and -1 value
'''

def outlier_removal_cont_data(iData):
	contData = iData
	for data in contData.columns.values:
		if np.sum(contData[data].isnull()) > 50:
			contData = contData.drop(data, axis = 1)
		elif np.sum(contData[data].isnull()) > 0:
			median = contData[data].median()
			idx = np.where(contData[data].isnull())[0]
			contData[data].iloc[idx] = median

			outliers = np.where(is_outlier(contData[data]))
			contData[data].iloc[outliers] = median
		
			if skew(contData[data]) > 0.75:
				contData[data] = np.log(contData[data])
				contData[data] = contData[data].apply(lambda x: 0 if x == -np.inf else x)
		
			contData[data] = Normalizer().fit_transform(contData[data].reshape(1,-1))[0]

	return contData

'''
	Outlier removal rules for categorical data-
	1. if missing data is more than 50 for a column = Drop the column
	2. if missing data is less than 50 for a column = Replace with DNA (Data not available)
	3. use LabelEncoder from sklearn
	4. determine number of unique values in each categorical column, create new column for binary
'''

def outlier_removal_cat_data(iData):
	catData = iData

	for data in catData.columns.values:
		if np.sum(catData[data].isnull()) > 50:
			catData = catData.drop(data,axis=1)
			continue
		elif np.sum(catData[data].isnull()) > 0:
			catData[data] = catData[data].fillna('DNA')

		catData[data] = LabelEncoder().fit_transform(catData[data])

		colMax = catData[data].max()

		for i in range(colMax):
			colName = data + '_' + str(i)
			catData[colName] = catData[data].apply(lambda x: 1 if x==i else 0)

		catData = catData.drop(data,axis=1)

	return catData




