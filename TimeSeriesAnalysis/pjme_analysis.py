# Time Series Forecast on Energy Consumption
# Dataset is composed of power consumption data from PJM’s website. PJM is a regional transmission organization in the United States
# Link to the dataset: https://www.kaggle.com/robikscube/hourly-energy-consumption

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
from xgboost import plot_importance, plot_tree
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf



def create_features(df, label=None):
    """
    Creates time series features from datetime index
    """
    df['date'] = df.index
    df['hour'] = df['date'].dt.hour
    df['dayofweek'] = df['date'].dt.dayofweek
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['dayofyear'] = df['date'].dt.dayofyear
    df['dayofmonth'] = df['date'].dt.day
    df['weekofyear'] = df['date'].dt.weekofyear
    
    X = df[['hour','dayofweek','quarter','month','year',
           'dayofyear','dayofmonth','weekofyear']]
    if label:
        y = df[label]
        return X, y
    return X

# Dataset description: 
# PJM East Region: 2001-2018 (PJME)
# hourly estimated energy consumption in Megawatts (MW)

pjme_dataframe = pd.read_csv('PJME_hourly.csv', index_col=[0], parse_dates=[0])
print(pjme_dataframe.head() )
print(pjme_dataframe.describe() )

plot_acf(pjme_dataframe['PJME_MW'], lags=168)
plt.grid(True)
plt.show()