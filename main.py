# main.py from project CREDIT_PUNCTUATION_MODEL created by Emiliano Mena González on 12/02/2024.
# This file includes all the proccess to get the expected results of the project. In this case we have the
# application of the data cleaning and model punctuation functions developed on functions.py.

## Libraries and dependencies
from data import df
import functions as f
import pandas as pd
import numpy as np

## Data cleaning
data_info = f.analyse_data(df) # Analyse the data
drop_vars = ['ID','Month','Age','SSN','Occupation','Num_Bank_Accounts','Num_Credit_Card','Num_of_Loan',
             'Type_of_Loan','Payment_of_Min_Amount','Payment_Behaviour'] # Variables to drop
df2 = df.drop(columns = drop_vars, axis = 1) # Drop the variables that won´t be used
cus_vars = ['Name','Annual_Income','Monthly_Inhand_Salary','Interest_Rate','Credit_Mix','Credit_History_Age']
for var in cus_vars: # Fill the variables with the info of the same Customer
   df2[var] = f.fill_info_same_customer(data = df2, id_var = 'Customer_ID', fill_var = var)
cero_vars = ['Num_of_Delayed_Payment','Num_Credit_Inquiries','Amount_invested_monthly','Monthly_Balance']
for var in cero_vars: # Fill the variables with 0
   df2[var] = f.fill_ceros(data = df2, var = var)
num_vars = ['Annual_Income','Num_of_Delayed_Payment','Changed_Credit_Limit','Outstanding_Debt',
            'Amount_invested_monthly','Monthly_Balance']
for var in num_vars: # Convert string numbers to float numbers
   df2[var] = [f.only_numbers(x) for x in df2[var]]
df2['Credit_History_Age'] = f.numeric_age(data = df2, var = 'Credit_History_Age')# Get the number of months
data_info_2 = f.analyse_data(df2) # Analyse to see if the data is ready

## Punctuation
model_variables = ['Delay_from_due_date','Num_of_Delayed_Payment','Total_EMI_per_month', # Payment history 30%
                   'Outstanding_Debt', # Amounts owed 20%
                   'Credit_History_Age', # Lengh of credit history 15%
                   'Credit_Mix', # Credit mix 10%
                   'Changed_Credit_Limit','Num_Credit_Inquiries', # New credit 15%
                   'Credit_Utilization_Ratio'] # Credit utilization 10%
scores = [[100,75,50,25,12.5],[100,80,60,40,20],[100,75,50,25,12.5],[200,185,165,100,50,35],
          [22.5,45,67.5,90,127.5,150],[100,50,15],[75,63.75,45,33.75,22.5],[75,63.75,45,33.75,22.5],
          [75,100,75,50,25,12.5]]
ranges = [[3,10,30,60,90],[1,7,13,19],[500,1000,2000,3000],[500,1000,1500,2000,2500],[24,48,72,96,120],
          ['Good','Standard'],[100,60,40,20],[2,6,10,14],[20,35,40,50,70]]
conditions = [0,0,2,0,0,1,0,0,0]
model_data = [df2[v].values for v in model_variables]
variables_punctuation = [f.punctuation(s,r,m,c) for s,r,m,c in zip(scores,ranges,model_data,conditions)]
model_punctuation = f.final_punctuation(variables_punctuation)
model_score = f.score(['Poor','Standard','Good'], [300,800], model_punctuation)
results = f.df_results(df2, model_punctuation, model_score)
accuracy = f.accuracy(model_score, df2)

## Separe the data on train and test (No se si es necesario o no)
# df_train = df.sample(frac=0.8)
# df_test = df.drop(df_train.index)
# Variables didn´t used ['Annual_Income','Monthly_Inhand_Salary','Interest_Rate','Amount_invested_monthly']