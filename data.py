# On this file the databases will be loaded, on this project we have only one database that is on a csv
# file named 'train.csv'

# Libraries and dependencies
import pandas as pd

# Load the train database
df = pd.read_csv('files/train.csv',low_memory=False)