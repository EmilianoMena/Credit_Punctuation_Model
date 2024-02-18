# main.py from project CREDIT_PUNCTUATION_MODEL created by Emiliano Mena González on 12/02/2024.
# This file includes all the proccess to get the expected results of the project. In this case we have the
# application of the data cleaning and model punctuation functions developed on functions.py.

## Libraries and dependencies
from data import df
import functions as f

## Data cleaning
data_info = f.analyse_data(df) # Analyse the data
drop_variables = ['ID','Month','Age','SSN','Occupation','Num_Bank_Accounts','Num_Credit_Card','Num_of_Loan',
             'Type_of_Loan','Payment_of_Min_Amount','Payment_Behaviour'] # Variables to drop
df2 = df.drop(columns = drop_variables, axis = 1) # Drop the variables that won´t be used
customer_variables = ['Name','Annual_Income','Monthly_Inhand_Salary','Interest_Rate','Credit_Mix',
                      'Credit_History_Age']
for var in customer_variables: # Fill the variables with the info of the same Customer
   df2[var] = f.fill_info_same_customer(data = df2, id_var = 'Customer_ID', fill_var = var)
cero_variables = ['Num_of_Delayed_Payment','Num_Credit_Inquiries','Amount_invested_monthly','Monthly_Balance']
for var in cero_variables: # Fill the variables with 0
   df2[var] = f.fill_ceros(data = df2, var = var)
numeric_variables = ['Annual_Income','Num_of_Delayed_Payment','Changed_Credit_Limit','Outstanding_Debt',
            'Amount_invested_monthly','Monthly_Balance']
for var in numeric_variables: # Convert string numbers to float numbers
   df2[var] = [f.only_numbers(x) for x in df2[var]]
df2['Credit_History_Age'] = f.numeric_age(data = df2, var = 'Credit_History_Age')# Get the number of months
outliers_variables = ['Annual_Income','Interest_Rate','Num_of_Delayed_Payment','Num_Credit_Inquiries',
                      'Total_EMI_per_month','Amount_invested_monthly','Monthly_Balance']
data_stadistics = df2.describe()
df3 = df2.copy()
for var in outliers_variables: # Replace the outliers
   df3[var] = f.outliers_replace(df3,var,1)

## Punctuation
model_variables = ['Delay_from_due_date','Num_of_Delayed_Payment', # Payment history 35%
                   'Outstanding_Debt', # Amounts owed 30%
                   'Credit_History_Age', # Lengh of credit history 10%
                   'Credit_Mix', # Credit mix 15%
                   'Num_Credit_Inquiries'] # New credit 10%
scores = [[200,150,100,75,50,25],[150,120,90,60,30],[300,275,250,150,75,50],[15,30,45,60,85,100],[150,100,50],
          [100,85,60,45,30]]
ranges = [[3,10,30,60,90],[1,7,13,19],[500,1000,1500,2000,2500],[24,48,72,96,120],['Good','Standard'],
          [2,6,10,14]]
conditions = [0,0,0,0,1,0]
model_data = [df3[v].values for v in model_variables]
variables_punctuation = [f.punctuation(s,r,m,c) for s,r,m,c in zip(scores,ranges,model_data,conditions)]
model_punctuation = f.final_punctuation(variables_punctuation)
model_score = [f.score(600,800,x) for x in model_punctuation]
results = f.df_results(df3, model_punctuation, model_score)
accuracy = f.accuracy(model_score, df3)