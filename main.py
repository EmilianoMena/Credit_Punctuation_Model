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

## Punctuation
model_variables = ['Delay_from_due_date','Num_of_Delayed_Payment',#'Total_EMI_per_month', # Payment history 30%
                   'Outstanding_Debt', # Amounts owed 25%
                   'Credit_History_Age', # Lengh of credit history 15%
                   'Credit_Mix', # Credit mix 10%
                   'Changed_Credit_Limit','Num_Credit_Inquiries', # New credit 10%
                   'Credit_Utilization_Ratio'] # Credit utilization 10%
data_stadistics = pd.DataFrame([df2[x].describe() for x in model_variables])
scores = [[150,100,50,0],[150,100,50,0],[250,175,100,25,0],[50,60,80,100],[100,75,50],[50,40,30,20],[50,40,30,20,10],[50,100,50,0]]
ranges = [[0,3,15],[0,5,10],[250,500,750,1000],[24,48,120,240],['Good','Standard'],[2,4,6],[3,6,9,12],[25,30,35]]
conditions = [0,0,2,0,0,1,0,0,0]
model_data = [df2[v].values for v in model_variables]
variables_punctuation = [f.punctuation(s,r,m,c) for s,r,m,c in zip(scores,ranges,model_data,conditions)]
model_punctuation = f.final_punctuation(variables_punctuation)
model_score = f.score(['Poor','Standard','Good'], [550,750], model_punctuation)
results = f.df_results(df2, model_punctuation, model_score)
accuracy = f.accuracy(model_score, df2)

#Variables didn´t used ['Annual_Income','Monthly_Inhand_Salary','Interest_Rate','Amount_invested_monthly']