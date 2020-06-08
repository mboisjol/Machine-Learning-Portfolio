# From: https://medium.com/diogo-menezes-borges/project-3-analytics-vidhya-hackaton-black-friday-f6c6bf3da86f
#  Analytics Vidhya Black Friday hackathon

import pandas as pd
import numpy as np
import dask.dataframe as dd

import matplotlib.pyplot as plt
import seaborn as sns

import holidays

import xgboost as xgb
from xgboost import plot_importance, plot_tree
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf

from datetime import date
import time

# Reading the training dataframe
start_time = time.clock()
train_dataframe = dd.read_csv("train.csv")
test_dataframe = dd.read_csv("test.csv")
print(time.clock() - start_time, "seconds")

print(train_dataframe.head() )
print(train_dataframe.describe().compute() )
#print(train_dataframe.shape[0].compute() )

"""
# Check for duplicates
idsUnique = len( train_dataframe['User_ID'].drop_duplicates().compute() )
idsTotal = train_dataframe.shape[0].compute()
idsDupli = idsTotal - idsUnique
print("There are " + str(idsDupli) + " duplicate IDs for " + str(idsTotal) + " total entries")

# Distribution of the target variable: Purchase
plt.style.use('fivethirtyeight')
plt.figure(figsize=(12,7))
sns.distplot(train_dataframe.Purchase, bins = 25)
plt.xlabel("Amount spent in Purchase")
plt.ylabel("Number of Buyers")
plt.title("Purchase amount Distribution")
plt.show()

sns.countplot(train_dataframe['Occupation'].compute())
plt.show()

# Occupation vs Average purchase
Occupation_pivot = train_dataframe.groupby('Occupation')['Purchase'].mean().compute()
Occupation_pivot = Occupation_pivot.sort_index()
print(Occupation_pivot)

Occupation_pivot.plot(kind='bar', color='blue',figsize=(12,7))
plt.xlabel("Occupation")
plt.ylabel("Average Purchase")
plt.title("Occupation and Purchase Analysis")
plt.xticks(rotation=0)
plt.show()
"""

# Join Train and Test Dataset
train_dataframe['source']='train'
test_dataframe['source']='test'
data = dd.concat([train_dataframe,test_dataframe])
print(train_dataframe.shape, test_dataframe.shape, data.shape)

#Check the percentage of null values per variable
# only features having missing values: Product_Category_1 and Product_Category_2
print(data.isnull().sum().compute()/data.shape[0].compute()*100 )

# Imputing value 0
data["Product_Category_2"] = data["Product_Category_2"].fillna(-2.0).astype("float")
data["Product_Category_3"] = data["Product_Category_3"].fillna(-2.0).astype("float")

print(data.Product_Category_2.value_counts().compute().sort_index() )
print(data.Product_Category_3.value_counts().compute().sort_index() )




