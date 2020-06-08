
import pandas as pd
import numpy as np
import dask.dataframe as dd

import matplotlib.pyplot as plt
import seaborn as sns

import xgboost as xgb
from xgboost import plot_importance, plot_tree

from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf

from datetime import date
import time

# Reading the training dataframe
letters_dataframe = pd.read_csv("letters.csv")
print(letters_dataframe.head() )
print(letters_dataframe.shape )


features = letters_dataframe.columns[:-1]
X = letters_dataframe[features]
Y = letters_dataframe['label']

print(X.head() )

X_train, X_test, Y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

#clf_svm = LinearSVC(penalty="l2", dual=False, tol=1e-5)
clf_svm = svm.SVC(gamma = 0.01)

clf_svm.fit(X_train, Y_train)
y_pred_svm = clf_svm.predict(X_test)

def summarize_classification(y_test, 
                             y_pred, 
                             avg_method='weighted'):
    
    acc = accuracy_score(y_test, y_pred,normalize=True)
    num_acc = accuracy_score(y_test, y_pred,normalize=False)

    prec = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    
    print("Test data count: ",len(y_test))
    print("accuracy_count : " , num_acc)
    print("accuracy_score : " , acc)
    print("precision_score : " , prec)
    print("recall_score : ", recall)

summarize_classification(y_test, y_pred_svm)

# Distribution of the target variable
length_bins = len(set(y_test))
print(length_bins)


plt.style.use('fivethirtyeight')
plt.figure(figsize=(10,5))
plt.scatter(y_test, y_pred_svm )
#, cmap=plt.cm.jet)

plt.show()

#print(y_test)
#print(y_pred_svm)


#acc_svm = accuracy_score(y_test, y_pred_svm)
#print ('SVM accuracy: ',acc_svm)