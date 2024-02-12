# The main file is where the data and functions are used to get the final results

# Libraries and dependencies
from data import df
import functions as f

# First the data analyse to see what data we have
DA = f.analyse_data(df)

# Separate the variables that will not be consider on the model
drop_vars = ['ID','Month','Age','SSN','Occupation','Type_of_Loan','Payment_Behaviour','Num_Bank_Accounts',
             'Num_Credit_Card','Num_of_Loan']

# Drop the columns of the dataframe
df2 = df.drop(columns = drop_vars, axis = 1)

# Identify the object variables
obj_vars = ['Name','Credit_Mix','Credit_Score']

# Remove punctuation and whitespaces
for x in obj_vars:
    df2[x] = [f.remove_punctuation(y) for y in df2[x]]
    df2[x] = [f.remove_whitespace(y) for y in df2[x]]
    df2[x] = [f.remove_whitespace_lr(y) for y in df2[x]]
    df2[x] = df2[x].replace('_',method='ffill')
    df2[x] = df2[x].fillna(method='ffill')

# Identify the numerical values
num_vars = ['Annual_Income','Monthly_Inhand_Salary', 'Interest_Rate','Delay_from_due_date',
            'Num_of_Delayed_Payment','Changed_Credit_Limit','Num_Credit_Inquiries','Outstanding_Debt',
            'Credit_Utilization_Ratio', 'Credit_History_Age','Total_EMI_per_month','Amount_invested_monthly',
            'Monthly_Balance']

# Change the 'Credit_History_Age' from 'N Years and N Months' to N months, fill the NA values with the last
# value of the same 'Customer_ID'
df2['Credit_History_Age'] = f.numeric_age(df2['Credit_History_Age'])

# Change all the numerical variables to numerical values and replace '_' to 0
for x in num_vars:
   df2[x] = df2[x].replace('_',0)
   df2[x] = f.numerical_values(df2[x])