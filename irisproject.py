# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 21:50:32 2018

@author: samse
"""

import sys
print('Python: {}'.format(sys.version))
# scipy
import scipy
print('scipy: {}'.format(scipy.__version__))
# numpy
import numpy
print('numpy: {}'.format(numpy.__version__))
# matplotlib
import matplotlib
print('matplotlib: {}'.format(matplotlib.__version__))
# pandas
import pandas
print('pandas: {}'.format(pandas.__version__))
# scikit-learn
import sklearn
print('sklearn: {}'.format(sklearn.__version__))




# Load libraries
import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

#https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
#column names
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(url, names=names)
url2 = "C:\\Users\\samse\\Documents\\GitHub\\iris.csv"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset2 = pandas.read_csv(url2, names=names)

#shape 
print(dataset.shape)

print(dataset.describe())

#class distribution
print(dataset.groupby('class').size())


# box and whisker plots
dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
plt.show()



# histograms
dataset.hist()
plt.show()

# histograms
dataset.hist()
plt.show()



# scatter plot matrix
scatter_matrix(dataset)
plt.show()

# scatter plot matrix
scatter_matrix(dataset)
plt.show()