"""
Created on Mon Nov 13 12:28:24 2017

@author: Erik
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import summary

def normalize(iData):

    
    iData = add_yn_feature(iData, 'HasLotFrontage', 'LotFrontage')
    iData = add_yn_feature(iData, 'HasBsmt', 'TotalBsmtSF')
    iData = add_yn_feature(iData, 'HasPool', 'PoolArea')
    iData = add_yn_feature(iData, 'HasGarage', 'GarageArea')
    
    iData = take_logs(iData)
 
    
    #unnecessary features
    iData = iData.drop('MiscFeature', 1)
    iData = iData.drop( 'MiscVal', 1)
    iData = iData.drop('Id', 1)
    iData = iData.drop('PID', 1)
    
    #add 0 1 encoding
    iData = pd.get_dummies(iData)
    
    remove_correlated_features(iData)
    
    return iData

def take_logs(iData):
    iData = take_log(iData, 'SalePrice')
    iData = take_log(iData, 'GrLivArea')
    iData = take_log(iData, '1stFlrSF')
    return iData
    
    
def remove_correlated_features(iData):
    #highly correlated with greatliveara
    
    iData = iData.drop('TotRmsAbvGrd', 1)
    
    #highly correlated with Garage Cars
    iData = iData.drop('GarageArea', 1)
    
    #highly correlated with year built
    iData = iData.drop('GarageYrBlt', 1)
    
    iData = iData.drop('TotalBsmtSF', 1)
    
    return iData

# Function to impute missing values
def feat_impute(iData, columns):
    for column in columns:
        if iData[column].dtype ==np.object:
            iData.loc[iData[column].isnull(),column] = 'None'
        else:
            iData.loc[iData[column].isnull(),column] = 0
            
    return iData

def fill_in_missing_values(iData):
    values = {}
    col_type_list = summary.missing_data(iData)
    for index, row in col_type_list.iterrows():
        if (row.Total == 0):
            break
        #if(index == 'LotFrontage'):
            #values[index] = 69.79
        if(row.DataType == 'object'):
            values[index] = 'NotApplicable'
        else:
            values[index] = 0
    
    return iData.fillna(value = values)
        

def add_yn_feature(iData, feature, based_on):
    #creates feature with your feature name that has a value of 1 where
    # the based on feature is greater than  0
    iData[feature] = pd.Series(len(iData[based_on]), index=iData.index)
    iData[feature] = 0 
    iData.loc[iData[based_on]> 0,feature] = 1
    return iData

def take_nonzero_log(iData, feature):
    temp = iData.loc[iData[feature]>0]
    
    iData.loc[iData[feature]>0,feature] = np.log(temp[feature])
    iData = iData.rename(columns = {feature: 'log_' + feature})
    return iData
    
def take_log(iData, feature):
    iData[feature] = np.log(iData[feature])
    iData = iData.rename(columns = {feature: 'log_' + feature})
    return iData
    
    
def drop_cols_with_missing_data(iData):
    total = iData.isnull().sum().sort_values(ascending=False)
    percent = (iData.isnull().sum()/iData.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    return iData.drop((missing_data[missing_data['Percent'] >= 0.50]).index,1)

def handle_missing_data(iData):
    
    # columns with more than 50% missing data
    iData = drop_cols_with_missing_data(iData)
    
    print(iData.columns)
    #impute features with appropriate values
    
    # fireplace
    iData['FireplaceQu'] = iData['FireplaceQu'].fillna('None')
    
    # lot frontage
    iData['LotFrontage'] = iData['LotFrontage'].fillna(iData['LotFrontage'].median())
    
    # garageX variable
    iData = feat_impute(iData, ['GarageYrBlt','GarageType','GarageQual','GarageCond','GarageFinish'])
    iData = feat_impute(iData, ['GarageCars','GarageArea'])
    
    # Basement Data
    iData = feat_impute(iData, ['BsmtFinSF1','BsmtUnfSF','BsmtFinSF2'])
    iData = feat_impute(iData, ['BsmtFinType2','BsmtFinType1', 'BsmtExposure', 'BsmtCond','BsmtQual' ])
    iData = feat_impute(iData, ['BsmtHalfBath','BsmtFullBath'])
    iData = feat_impute(iData, ['TotalBsmtSF'])
    
    # can be done using criteria on BsmtFinType2 = 'Unf'
    iData.iloc[1420, iData.columns.get_loc('BsmtExposure')] = 'No'
    iData.iloc[1940, iData.columns.get_loc('BsmtExposure')] = 'No'
    
    # electrical - only one value missing - impute with mode
    iData['Electrical'] = iData['Electrical'].fillna(iData['Electrical'].mode()[0])
    
    # impute masonry data
    iData['MasVnrArea'] = iData['MasVnrArea'].fillna(iData['MasVnrArea'].mode()[0])
    iData['MasVnrType'] = iData['MasVnrType'].fillna(iData['MasVnrType'].mode()[0])
    
    print(iData.shape)
    return iData
    
    