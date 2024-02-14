# This file includes all the data neccessary to develop the project. 
# In this case it is required only 1 database that is called 'train.csv', this database includes data of a 
# credit punctuation based on a set of variables.

## Libraries and dependencies
import pandas as pd

## Load the train database
df = pd.read_csv('files/train.csv',low_memory=False)
## Separe the data on train and test
#df_train = df.sample(frac=0.8)
#df_test = df.drop(df_train.index)