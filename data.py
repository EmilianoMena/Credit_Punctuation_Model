# data.py from project CREDIT_PUNCTUATION_MODEL created by Emiliano Mena González and Jorge Alberto 
# Hernández Hernández on 12/02/2024.
# This file includes all the data neccessary to develop the project, in this case the only data avalaible is
# 1 database contained in a csv file called 'train.csv'. This database has credit information of different
# people.

## Libraries and dependencies
import pandas as pd

## Load the train database
df = pd.read_csv('files/train.csv',low_memory=False)