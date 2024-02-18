# visualizations.py from project CREDIT_PUNCTUATION_MODEL created by Emiliano Mena González on 12/02/2024.
# This file includes all the graphs and visual supports to present the results of the project. In this case
# the only visualization is going to be a confusion matrix.

## Libraries and dependencies
from main import results
from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt

## Confusion matrix
original = results['Original_Score']
model = results['Model_Score']
confusion_matrix = metrics.confusion_matrix(original, model)
heatmap = sns.heatmap(confusion_matrix, annot=True, fmt='g', xticklabels=['Poor', 'Standard','Good'], 
                      yticklabels=['Poor', 'Standard','Good'])
graph1 = plt.ylabel('Model',fontsize=13)
graph1 = plt.xlabel('Original',fontsize=13)
graph1 = plt.title('Confusion Matrix',fontsize=17)