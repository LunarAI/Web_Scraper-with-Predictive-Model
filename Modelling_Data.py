import csv
import numpy as np 
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import random
import time
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier 
from sklearn.model_selection import train_test_split
from collections import defaultdict
#====================================
# Housekeeping						#
#====================================
mean = []
list_original = []
list_predicted = []
#===============================================================
# Create arrays with names of cols and numerical value of cars #
#===============================================================
names = ['Year','Make','Model','Mileage','Colour','Gear Type','Fuel Type','Price','UID']
arr_num = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
#====================================
# Errors that has to be deactivated #
#====================================
pd.options.mode.chained_assignment = None
import warnings
warnings.filterwarnings('ignore') 
#==============================================================================================
# Create a dataframe for each car in arr_num, which represents cars used in file: car_details #
# We run dataframe through model to produce predictions for every make                        #
#==============================================================================================
for num in arr_num:
	#================================================================================
	# Create dataframe for specific car and assign values to id, target,            #
	# categorical and numerical columns, generate features list from abovementioned #
	#================================================================================
	df_main = pd.read_csv('car_details/'+str(num)+'.csv',names = names,index_col='UID')
	ID_col = ['UID']
	target_col = ['Price']
	cat_cols = ['Make','Model','Colour','Gear Type','Fuel Type']
	num_cols = ['Year','Mileage']
	features = list(set(list(df_main.columns))-set(ID_col)-set(target_col))
	#=======================================================
	# Label encoders for categorical columns and transform #
	# Need to save encoder for decoding					   #
	#=======================================================
	for var in cat_cols:
		encoder = LabelEncoder() 
		df_main[var] = encoder.fit_transform(df_main[var].astype('str'))
		np.save('Encoders/classes'+var+'.npy', encoder.classes_)
	#================================
	#Split into train and test data #
	#================================
	df_train, df_test = train_test_split(df_main, test_size=0.33, random_state=42)
	x_train = df_train[list(features)].values
	y_train = df_train[list(target_col)].values
	x_test = df_test[list(features)].values
	y_validate = df_test[list(target_col)]
	#======================
	#Create random forest #
	#======================
	random.seed(time.time())
	rf = RandomForestClassifier(n_estimators = 1000)
	model = rf.fit(x_train, y_train.ravel())
	#==============================
	# Final model and predictions #
	# Raw stored in csv file      #
	#==============================
	final_status = model.predict(x_test)
	df_test[target_col] = final_status
	df_test.to_csv('Output/Raw/model_output'+str(num)+'.csv')
	#==============================================================
	# Calculate standard deviation of dataset to measure          #
	# accuracy since roc_auc doesn't support multiclass functions #
	#==============================================================
	#=======================
	# Cast to float first  #
	#=======================
	y_predicted = df_test[target_col]
	l_validate = y_validate['Price'].values.tolist()
	l_predicted = y_predicted['Price'].values.tolist()
	counter = 0
	for number in l_validate:
		l_validate[counter] = number.replace(' ','')
		l_predicted[counter] = l_predicted[counter].replace(' ','')
		list_original.append(float(l_validate[counter]))
		list_predicted.append(float(l_predicted[counter]))
		counter += 1
	#=============================
	# Standard deviation of data #
	#=============================
	counter = 0
	for number in list_original:
		ans = (number - list_predicted[counter])**2
		mean.append(ans)
		counter += 1
	accuracy = round(np.sqrt(np.sum(mean)/counter),2)
	#================================================================
	# Convert back to readable data using stored conversion classes #
	# and store in csv file                                         #
	#================================================================
	df_convert = df_test
	for var in cat_cols:
		encoder.classes_ = np.load('Encoders/classes'+var+'.npy')
		arrConv = encoder.inverse_transform(df_convert[var].astype('int'))
		df_convert[var] = arrConv
	df_convert = df_convert.assign(Original_Prices=y_validate)
	df_convert = df_convert.assign(Standard_Deviation='')
	df_convert.at['Standard_Deviation','Standard_Deviation'] = accuracy
	df_convert.to_csv('Output/Converted/model_output'+str(num)+'.csv')
