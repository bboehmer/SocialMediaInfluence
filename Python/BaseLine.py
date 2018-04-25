#!/usr/bin/python
# -*- coding: utf8 -*-

# SAMPLE SUBMISSION TO THE BIG DATA HACKATHON 13-14 April 2013 'Influencers in a Social Network'
# .... more info on Kaggle and links to go here
#
# written by Ferenc Huszár, PeerIndex

import numpy as np
from sklearn import linear_model
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve


import matplotlib.pyplot as plt
from itertools import cycle
from scipy import interp
from sklearn import svm, datasets
from sklearn.metrics import auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import mean_squared_error
from sklearn.datasets import make_friedman1
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from scipy import interp

###########################
# LOADING TRAINING DATA
###########################

trainfile = open('../train.csv')
header = trainfile.next().rstrip().split(',')

y_train = []
X_train_A = []
X_train_B = []

for line in trainfile:
    splitted = line.rstrip().split(',')
    label = int(splitted[0])
    A_features = [float(item) for item in splitted[1:12]]
    B_features = [float(item) for item in splitted[12:]]
    y_train.append(label)
    X_train_A.append(A_features)
    X_train_B.append(B_features)
trainfile.close()

#These lines double the amount of training data by entering the the opposite of every entry
#This increases accuracy by like 0.007 so decent increase but not insane
trainfile = open('../train.csv')
header = trainfile.next().rstrip().split(',')
for line in trainfile:
    splitted = line.rstrip().split(',')
    label = int(splitted[0])
    A_features = [float(item) for item in splitted[1:12]]
    B_features = [float(item) for item in splitted[12:]]
    if label == 0:
        y_train.append(1)
    else:
        y_train.append(0)
    X_train_A.append(B_features)
    X_train_B.append(A_features)
trainfile.close()

y_train = np.array(y_train)
X_train_A = np.array(X_train_A)
X_train_B = np.array(X_train_B)

###########################
# EXAMPLE BASELINE SOLUTION USING SCIKIT-LEARN
#
# using scikit-learn LogisticRegression module without fitting intercept
# to make it more interesting instead of using the raw features we transform them logarithmically
# the input to the classifier will be the difference between transformed features of A and B
# the method roughly follows this procedure, except that we already start with pairwise data
# http://fseoane.net/blog/2012/learning-to-rank-with-scikit-learn-the-pairwise-transform/
###########################

#X_train = np.log(1+X_train_A) - np.log(1+X_train_B)
X_train = np.log(1+X_train_A) - np.log(1+X_train_B)

random_state = np.random.RandomState(0)
classifier = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True,random_state=random_state))
classifier2 = OneVsRestClassifier(svm.SVC(kernel='rbf', probability=True,random_state=random_state))

clf = NearestCentroid()
clf.fit(X_train, y_train)
NearestCentroid(metric='euclidean', shrink_threshold=None)
y_score = clf.predict(X_train)
y_score2 = classifier.fit(X_train, y_train).decision_function(X_train)
y_score3 = classifier2.fit(X_train, y_train).decision_function(X_train)
y_score4 = GradientBoostingRegressor(n_estimators=200, learning_rate=1.9, max_depth=1, random_state=0).fit(X_train, y_train).predict(X_train)
y_score5 = RandomForestClassifier(n_estimators=100).fit(X_train, y_train).predict(X_train)
y_score6 = (y_score4+y_score5)/2

fpr = dict()
tpr = dict()
fpr2 = dict()
tpr2 = dict()
fpr3 = dict()
tpr3 = dict()
fpr4 = dict()
tpr4 = dict()
fpr5 = dict()
tpr5 = dict()
print("Accuracy on Training Data")
print("KNN")
print(roc_auc_score(y_train,y_score, average='macro',sample_weight=None))
print("One v Rest RBF")
print(roc_auc_score(y_train,y_score2, average='macro',sample_weight=None))
print("One v Rest Linear")
print(roc_auc_score(y_train,y_score3, average='macro',sample_weight=None))
print("Gradient Boosting Regression")
print(roc_auc_score(y_train,y_score4, average='macro',sample_weight=None))
print("Random Forest Classifier")
print(roc_auc_score(y_train,y_score5, average='macro',sample_weight=None))
print("Average")
print(roc_auc_score(y_train,y_score6, average='macro',sample_weight=None))

# plt.figure()
# lw = 2
# for i in range(len(X_train)):
#     fpr[i], tpr[i], _ = roc_curve(y_train, y_score)
#     fpr2[i], tpr2[i], _ = roc_curve(y_train, y_score2)
#     fpr3[i], tpr3[i], _ = roc_curve(y_train, y_score3)
#     fpr4[i], tpr4[i], _ = roc_curve(y_train, y_score4)
#     fpr5[i], tpr5[i], _ = roc_curve(y_train, y_score5)
#
# plt.plot(fpr[2], tpr[2], color='purple',
#          lw=lw, label='KNN (area = %0.5f)' % roc_auc_score(y_train,y_score, average='macro',sample_weight=None))
# plt.plot(fpr2[2], tpr2[2], color='red',
#          lw=lw, label='One v Rest RBF (area = %0.5f)' % roc_auc_score(y_train,y_score2, average='macro',sample_weight=None))
# plt.plot(fpr3[2], tpr3[2], color='darkorange',
#          lw=lw, label='One v Rest Linear (area = %0.5f)' % roc_auc_score(y_train,y_score3, average='macro',sample_weight=None))
# plt.plot(fpr4[2], tpr4[2], color='blue',
#          lw=lw, label='Gradient Boosting Regression (area = %0.5f)' % roc_auc_score(y_train,y_score4, average='macro',sample_weight=None))
# plt.plot(fpr5[2], tpr5[2], color='yellow',
#          lw=lw, label='Random Forest Classifier (area = %0.5f)' % roc_auc_score(y_train,y_score5, average='macro',sample_weight=None))
#
# plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Classifying Training Data')
# plt.legend(loc="lower right")
# plt.show()

###########################
# READING TEST DATA
###########################
testfile = open('../test.csv')
#ignore the test header
testfile.next()

X_test_A = []
X_test_B = []
for line in testfile:
    splitted = line.rstrip().split(',')
    A_features = [float(item) for item in splitted[0:11]]
    B_features = [float(item) for item in splitted[11:]]
    X_test_A.append(A_features)
    X_test_B.append(B_features)
testfile.close()

X_test_A = np.array(X_test_A)
X_test_B = np.array(X_test_B)

# transform features in the same way as for training to ensure consistency
X_test = np.log(1+X_test_A) - np.log(1+X_test_B)

y_scoreG = GradientBoostingRegressor(n_estimators=200, learning_rate=1.9, max_depth=1, random_state=0).fit(X_train, y_train).predict(X_test)
y_scoreR = RandomForestClassifier(n_estimators=100).fit(X_train, y_train).predict(X_test)
y_score = (y_scoreG+y_scoreR)/2


###########################
# WRITING SUBMISSION FILE
###########################

predfile = open('predictions.csv','w+')
#print >>predfile, y_score
for i in range(len(y_score)):
    if y_score[i]>1:
        print >>predfile, 1
    elif y_score[i]<0:
        print >>predfile, 0
    else:
        print >>predfile, y_score[i]

predfile.close()
