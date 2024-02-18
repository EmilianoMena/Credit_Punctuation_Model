# visualizations.py from project CREDIT_PUNCTUATION_MODEL created by Emiliano Mena González on 12/02/2024.
# This file includes all the graphs and visual supports to present the results of the project. In this case
# the only visualization is going to be a confusion matrix.

## Libraries and dependencies
from main import results, df2
from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt

## Violinplots
def violinplots(x : list):
    '''
    Create a violin plot to see outliers on the data

    Parameters
    ----------
        x : list
            The data that will be plot
        
    Returns
    -------
    plt
        The violin plot
    '''
    sns.violinplot(x)
    plt.show()

## Confusion matrix
def heatmap(original : list, model : list, labels : list):
    '''
    Create a violin plot to see outliers on the data

    Parameters
    ----------
        original : list
            The original data
        model : list
            The predicted data
        labels : list
            The different categories in which they were predicted the data
        
    Returns
    -------
    plt
        A heatmap plot
    '''
    confusion_matrix = metrics.confusion_matrix(original, model)
    sns.heatmap(confusion_matrix, annot=True, fmt='g', xticklabels=labels, yticklabels=labels).set(
        title='Confusion Matrix',xlabel='Original',ylabel='Model')
    plt.show()