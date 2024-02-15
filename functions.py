# This file contains the functions created to do certain process or operations.
# In this case the functions developed are separated on two parts of the project. First the data clean and
# analysis, and then the model punctuation.

## Libraries and dependencies
import pandas as pd
import numpy as np
import string

## Data Analysis and Data Cleaning
def analyse_data(data: pd.DataFrame ='Dataset that will be analysed'):
    '''
    The function returns information of the different variables that the dataset includes to proceed with
    the data cleaning. The only parameter that the function asks for is the dataset declared as data.
    '''
    df = pd.DataFrame({
        'Variable_name':list(data.columns.values), # Name of the variable (column)
        'Type':list(data.dtypes), # Type of data
        'NA_values':list(data.isnull().sum()), # Null values
        'Present_values':list(data.count()), # Number of values each variable has
        'Unique_values':[data[x].nunique() for x in data.columns.values], # Unique values of each variable
    }).set_index('Variable_name')
    return df

def fill_info_same_customer(data: pd.DataFrame ='Dataset that will be analysed',
                            id_var: str = 'Variable that identifies the person',
                            fill_var: str = 'Variable that will be filled or replaced'):
    '''
    The function fill the null values and replace the modified values with the information of the same
    person. The parameters that the function needs are the dataset, the variable that identifies the person
    and the variable that the values will be filled or replaced.
    '''
    k = list(data[id_var].bfill())
    v = list(data[fill_var].bfill())
    c = {x:y for x,y in zip(k,v)}
    result = [c.get(x,0) for x in k]
    return result

def fill_ceros(data: pd.DataFrame ='Dataset that will be analysed',
               var: str = 'Variable that null values would be filled with 0'):
    '''
    The function fills the variables null values with 0. It has 2 parameters, first the dataset and second
    the variable.
    '''
    result = data[var].fillna(0)
    return result

def only_numbers(var: str = 'String that has a number'):
    '''
    The function receives a string that contains numbers and punctuaction or other elements and returns
    the only the number on float format. The only parameter is the string.
    '''
    try:
        var = ''.join(ch for ch in var if ch in string.digits+'.'+'-')
    except:
        pass
    result = [float(0) if var=='' or var=='.' or var=='-' or var=='-.' else float(var)][0]
    return result

def numeric_age(data: pd.DataFrame ='Dataset that contains the variable',
                var: str = 'Variable of the age that will be converted to numeric'):
    '''
    The function converts the age from a format of NN Years to NN Months to numeric months. It receives the
    dataset and the variable that has the age.
    '''
    result = [int(xi[0])*12 + int(xi[3]) for xi in [x.split() for x in data[var]]]
    return result

## Punctuation functions
### FICO model
f1 = lambda x: 200 if x <= 3 else 150 if x <= 10 else 100 if x <= 30 else 75 if x <= 60 else 50 if x <= 90 else 25
f2 = lambda x: 150 if x <= 1 else 120 if x <= 7 else 90 if x <= 13 else 60 if x <= 19 else 30
f3 = lambda x: 300 if x <= 500 else 275 if x <= 1000 else 250 if x <= 1500 else 150 if x <= 2000 else 75 if x <= 2500 else 50 
f4 = lambda x: 15 if x <= 24 else 30 if x <= 48 else 45 if x <= 72 else 60 if x <= 96 else 85 if x <=120 else 100
f5 = lambda x: 150 if x == 'Good' else 75 if x == 'Standard' else 25
f6 = lambda x: 100 if x <= 2 else 85 if x <= 6 else 60 if x <= 10 else 45 if x <= 14 else 30
f7 = lambda x: 50 if x <= 50 else 0
f8 = lambda x: 50 if x<= 30 else 0
### Altman Z-score
fx1 = lambda x,y,z : [xi / (yi + zi) for xi,yi,zi in zip(x,y,z)]
fx2 = lambda x,y,z : [xi / (yi + zi) for xi,yi,zi in zip(x,y,z)]
fx3 = lambda x,y,z : [xi / (yi + zi) for xi,yi,zi in zip(x,y,z)]
fx4 = lambda x,y : [xi/ 12 / yi for xi,yi in zip(x,y)]
fx5 = lambda x,y,z : [xi / (yi + zi) for xi,yi,zi in zip(x,y,z)]
fz_score = lambda x1,x2,x3,x4,x5 : 1.2*x1 + 1.4*x2 + 3.3*x3 + 0.6*x4 + x5
alt_score = lambda x: 1000 if x > 3 else 650 if x > 1.8 else 300
### Final Score
final_score = lambda x: 'Poor' if x < 600 else 'Standard' if x < 800 else 'Good' 