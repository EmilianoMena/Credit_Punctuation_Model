# The main file is where the data and functions are used to get the final results

## Libraries and dependencies
import pandas as pd
from data import df
import functions as f

## Data cleaning
### Analyse the data
DA = f.analyse_data(df) 
### Separate the variables that will not be consider on the model
drop_vars = ['ID','Month','Age','SSN','Occupation','Type_of_Loan','Payment_Behaviour','Num_Bank_Accounts',
             'Num_Credit_Card','Num_of_Loan']
### Drop the columns of the dataframe
df2 = df.drop(columns = drop_vars, axis = 1)
### Identify the object variables
obj_vars = ['Name','Credit_Mix','Credit_Score']
### Remove punctuation and whitespaces
for x in obj_vars:
    df2[x] = [f.remove_punctuation(y) for y in df2[x]]
    df2[x] = [f.remove_whitespace(y) for y in df2[x]]
    df2[x] = [f.remove_whitespace_lr(y) for y in df2[x]]
    df2[x] = df2[x].replace('_',method='ffill')
    df2[x] = df2[x].fillna(method='ffill')
### Identify the numerical values
num_vars = ['Annual_Income','Monthly_Inhand_Salary', 'Interest_Rate','Delay_from_due_date',
            'Num_of_Delayed_Payment','Changed_Credit_Limit','Num_Credit_Inquiries','Outstanding_Debt',
            'Credit_Utilization_Ratio', 'Credit_History_Age','Total_EMI_per_month','Amount_invested_monthly',
            'Monthly_Balance']
### Change the 'Credit_History_Age' from 'N Years and N Months' to N months, fill the NA values with the last
### value of the same 'Customer_ID'
df2['Credit_History_Age'] = f.numeric_age(df2['Credit_History_Age'])
### Change all the numerical variables to numerical values and replace '_' to 0
for x in num_vars:
   df2[x] = df2[x].replace('_',0)
   df2[x] = f.numerical_values(df2[x])

## Punctuation
### FICO Model
FICO_vars = ['Delay_from_due_date','Num_of_Delayed_Payment','Outstanding_Debt','Credit_History_Age','Credit_Mix',
        'Num_Credit_Inquiries','Interest_Rate','Credit_Utilization_Ratio']
FICO_data = [df2[p].values for p in FICO_vars]
FICO_funcs = [f.f1,f.f2,f.f3,f.f4,f.f5,f.f6,f.f7,f.f8]
FICO_var_scores = [[fc(x) for x in xi]for xi,fc in zip(FICO_data,FICO_funcs)]
FICO_score = [sum(x) for x in zip(*FICO_var_scores)]
### Altman Z-score
x1 = [f.fx1(x,y,z) for x,y,z in zip(df2['Monthly_Balance'].values,df2['Monthly_Inhand_Salary'].values,df2['Total_EMI_per_month'].values)]
x2 = [f.fx2(x,y,z) for x,y,z in zip(df2['Amount_invested_monthly'].values,df2['Monthly_Inhand_Salary'].values,df2['Total_EMI_per_month'].values)]
x3 = [f.fx3(x,y,z) for x,y,z in zip(df2['Total_EMI_per_month'].values,df2['Monthly_Inhand_Salary'].values,df2['Total_EMI_per_month'].values)]
x4 = [f.fx4(x,y) for x,y in zip(df2['Annual_Income'].values,df2['Outstanding_Debt'].values)]
x5 = [f.fx5(x,y,z) for x,y,z in zip(df2['Monthly_Inhand_Salary'].values,df2['Monthly_Inhand_Salary'].values,df2['Total_EMI_per_month'].values)]
z_score = [f.fz_score(a,b,c,d,e) for a,b,c,d,e in zip(x1,x2,x3,x4,x5)]
alt_score = [f.alt_score(x) for x in z_score]
### Final Score
final_punct = [(x+y)/2 for x,y in zip(FICO_score,alt_score)]
final_score = [f.final_score(x) for x in final_punct]
### Results
results = pd.DataFrame({
    'Name': df2['Name'],
    'FICO_Punctuation': FICO_score,
    'Altman_Z-score': z_score,
    'Altman_Punctuation': alt_score,
    'Final_Punctuation': final_punct,
    'Final_Score': final_score,
    'Original_Score': df2['Credit_Score']
})
accuracy = [1 if x==y else 0 for x,y in zip(final_score,df2['Credit_Score'])]