# This file includes all the proccess to get the expected results of the project.
# In this case the data will be cleaned and analysed first and then it will be structured the punctuation
# and final score of the model.

## Libraries and dependencies
from data import df
import functions as f
import pandas as pd
import numpy as np

## Data cleaning
### Analyse the data
data_info = f.analyse_data(df) 
### Drop the variables that won´t be used
drop_vars = ['ID','Month','Age','SSN','Occupation','Num_Bank_Accounts','Num_Credit_Card','Num_of_Loan',
             'Type_of_Loan','Payment_of_Min_Amount','Payment_Behaviour']
df2 = df.drop(columns = drop_vars, axis = 1)
### Fill the variables with the info of the same Customer
cus_vars = ['Name','Annual_Income','Monthly_Inhand_Salary','Interest_Rate','Credit_Mix','Credit_History_Age']
for var in cus_vars:
   df2[var] = f.fill_info_same_customer(data = df2, id_var = 'Customer_ID', fill_var = var)
### Fill the variables with 0
cero_vars = ['Num_of_Delayed_Payment','Num_Credit_Inquiries','Amount_invested_monthly','Monthly_Balance']
for var in cero_vars:
   df2[var] = f.fill_ceros(data = df2, var = var)
### Convert string numbers to float numbers
num_vars = ['Annual_Income','Num_of_Delayed_Payment','Changed_Credit_Limit','Outstanding_Debt',
            'Amount_invested_monthly','Monthly_Balance']
for var in num_vars:
   df2[var] = [f.only_numbers(x) for x in df2[var]]
### Get the number of months of Credit History Age
df2['Credit_History_Age'] = f.numeric_age(data = df2, var = 'Credit_History_Age')
### Analyse the clean data
data_info_2 = f.analyse_data(df2) 

## Punctuation
### FICO Model
FICO_vars = ['Delay_from_due_date','Num_of_Delayed_Payment','Outstanding_Debt','Credit_History_Age','Credit_Mix',
        'Num_Credit_Inquiries','Interest_Rate','Credit_Utilization_Ratio']
FICO_data = [df2[p].values for p in FICO_vars]
FICO_funcs = [f.f1,f.f2,f.f3,f.f4,f.f5,f.f6,f.f7,f.f8]
FICO_var_scores = [[fc(x) for x in xi]for xi,fc in zip(FICO_data,FICO_funcs)]
FICO_score = [sum(x) for x in zip(*FICO_var_scores)]
# ### Altman Z-score
# x1 = f.fx1(df2['Monthly_Balance'].values,df2['Monthly_Inhand_Salary'].values,df2['Total_EMI_per_month'].values)
# x2 = f.fx2(df2['Amount_invested_monthly'].values,df2['Monthly_Inhand_Salary'].values,df2['Total_EMI_per_month'].values)
# x3 = f.fx3(df2['Total_EMI_per_month'].values,df2['Monthly_Inhand_Salary'].values,df2['Total_EMI_per_month'].values)
# x4 = f.fx4(df2['Annual_Income'].values,df2['Outstanding_Debt'].values)
# x5 = f.fx5(df2['Monthly_Inhand_Salary'].values,df2['Monthly_Inhand_Salary'].values,df2['Total_EMI_per_month'].values)
# z_score = [f.fz_score(a,b,c,d,e) for a,b,c,d,e in zip(x1,x2,x3,x4,x5)]
# alt_score = [f.alt_score(x) for x in z_score]
## Final Score
#final_punct = [(x+y)/2 for x,y in zip(FICO_score,alt_score)]
final_score = [f.final_score(x) for x in FICO_score]
### Results
results = pd.DataFrame({
    'Name': df2['Name'],
    'FICO_Punctuation': FICO_score,
    #'Altman_Z-score': z_score,
    #'Altman_Punctuation': alt_score,
    #'Final_Punctuation': final_punct,
    'Final_Score': final_score,
    'Original_Score': df2['Credit_Score']
})
accuracy = sum([1 if x==y else 0 for x,y in zip(final_score,df2['Credit_Score'])])/len(df2)
 
a = 'Changed_Credit_Limit'
