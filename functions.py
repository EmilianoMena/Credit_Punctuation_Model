# This file contains the functions created to do certain process or operations

## Libraries and dependencies
import pandas as pd
import numpy as np
import string
import data as d

## Data cleaning functions
def analyse_data(data): 
    df = pd.DataFrame({
        'Variable':list(data.columns.values),
        'Type':list(data.dtypes),
        'NA_values':list(data.isnull().sum()),
    })
    return df

def remove_punctuation(x):
        try:
            x=''.join(ch for ch in x if ch not in string.punctuation)
        except:
            pass
        return x

def remove_whitespace(x):
        try:
            x=''.join(x.split())
        except:
            pass
        return x

def remove_whitespace_lr(x):
        try:
            x=x.lstrip()
            x=x.rstirp()
        except:
            pass
        return x

def fill_null_values(data):
    return data.ffill()

def numeric_age(data):
    return [int(xi[0])*12 + int(xi[3]) for xi in [x.split() for x in fill_null_values(data)]]

def null_cero_values(data):
    return data.fillna(0)

def only_numbers(x):
    try:
        x=''.join(ch for ch in x if ch in string.digits)
    except:
        pass
    return x

def numerical_values(data):
    return [float(only_numbers(x)) for x in [xi for xi in null_cero_values(data)]]

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