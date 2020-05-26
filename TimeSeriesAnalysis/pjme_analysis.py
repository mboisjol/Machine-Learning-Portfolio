# Time Series Forecast on Energy Consumption
# Dataset is composed of power consumption data from PJM’s website. PJM is a regional transmission organization in the United States
# Link to the dataset: https://www.kaggle.com/robikscube/hourly-energy-consumption
# This file was inpired by robikscube tutorial: https://www.kaggle.com/robikscube/tutorial-time-series-forecasting-with-xgboost

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import holidays
import xgboost as xgb
from xgboost import plot_importance, plot_tree
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from datetime import date

def create_features(df, calendar, label=None):
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

	df['lag1'] = df['PJME_MW'].shift(1)
	df['lag24'] = df['PJME_MW'].shift(24)

	df['holidays'] = 0

	# Holiday verification
	for row, index in df.iterrows():

		year = row.year
		month = row.month
		day = row.day

		date_tmp = date(int(year), int(month), int(day))
		if( date_tmp in calendar):	
			df.at[row, 'holidays'] = 1

	# Drop NA values from lags
	df = df.dropna()
	
	X = df[['hour','dayofweek','quarter','month','year',
		   'dayofyear','dayofmonth','weekofyear', 'lag1', 'lag24', 'holidays']]
		   
	if label:
		y = df[label]
		return X, y, df
	return X, df

def mean_absolute_percentage_error(y_true, y_pred): 
    """Calculates MAPE given y_true and y_pred"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
	
# Dataset description: 
# PJM East Region: 2001-2018 (PJME)
# hourly estimated energy consumption in Megawatts (MW)

# Create US calendar
calendar = holidays.CountryHoliday('US')

pjme_dataframe = pd.read_csv('PJME_hourly.csv', index_col=[0], parse_dates=[0])
pjme_dataframe.index = pd.DatetimeIndex(pjme_dataframe.index)
pjme_dataframe = pjme_dataframe.sort_index()

# Printing info regarding the dataframe
print(pjme_dataframe )
print(pjme_dataframe.describe() )
print(pjme_dataframe.shape )

X_all, y_all, pjme_dataframe_lags = create_features(pjme_dataframe, calendar, label='PJME_MW')

# Auto-correlation visual
#plot_acf(pjme_dataframe['PJME_MW'], lags=168)
#plt.grid(True)
#plt.show()

# Rather to use a fixed date, specially if the times serie continues to grow, we set a train_test_split
# and find the appropriate index
train_test_split = 0.8
index_split = int(train_test_split*len(pjme_dataframe['PJME_MW']))
test_start = index_split+1

pjme_train = pjme_dataframe_lags.iloc[:index_split].copy()
X_train = X_all.iloc[:index_split].copy()
y_train = y_all.iloc[:index_split].copy()

#print(X_train)

pjme_test = pjme_dataframe_lags.iloc[index_split:].copy()
X_test = X_all.iloc[index_split:].copy()
y_test = y_all.iloc[index_split:].copy()

#print(X_test)

# XGBoost regressor
reg = xgb.XGBRegressor(n_estimators=1000, random_state = 42, objective = 'reg:squarederror')
reg.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], 
	early_stopping_rounds=50, verbose=False) # Change verbose to True if you want to see it train

# Predictions on test data and plot results
pmje_prediction = pd.DataFrame()
pmje_prediction['MW_Prediction'] = reg.predict(X_test)
pmje_prediction.index = pjme_test.index

plt.plot(pjme_dataframe.index, pjme_dataframe['PJME_MW'], label='PJME_MW')
plt.plot(pmje_prediction.index, pmje_prediction['MW_Prediction'], label='MW_Prediction')
plt.grid(True)
plt.ylabel('MW Consumption')
plt.xlabel('Time')
plt.legend()
plt.show()

# Training, testing scores and mean_absolute_percentage_error
print("Training Score : ", reg.score(X_train, y_train))
print("Calculate R-square score on test data : ", r2_score(y_test, pmje_prediction['MW_Prediction']) )
print("MAPE : ", mean_absolute_percentage_error(y_true=pjme_test['PJME_MW'], 
	y_pred=pmje_prediction['MW_Prediction']) )

# Results:
# Training Score :  0.9958982285262815
# Calculate R-square score on test data :  0.9950827298953134
# MAPE :  1.0726181128742815

# Feature importance plot
_ = plot_importance(reg, height=0.9)
plt.show()


# Taking a look at worst predicted days
pjme_test['MW_Prediction'] = pmje_prediction['MW_Prediction']
pjme_test['error'] = pjme_test['PJME_MW'] - pjme_test['MW_Prediction']
pjme_test['abs_error'] = pjme_test['error'].abs()
error_by_day = pjme_test.groupby(['year','month','dayofmonth']) \
    .mean()[['PJME_MW','MW_Prediction','error','abs_error']]

print(error_by_day.sort_values('error', ascending=True).head(10) )

	
