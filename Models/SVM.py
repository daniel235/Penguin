# To set seed random number in order to reproducable results in keras
from numpy.random import seed
seed(4)
import tensorflow
tensorflow.random.set_seed(1234)
########################################
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
import pandas as pd
from statistics import mean, median
import numpy as np
import sys
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn import svm
from numpy import *
from sklearn.preprocessing import MinMaxScaler #For feature scaling
import pickle


def runSVM(x):
    #load svm
    with open("svm.pkl", 'rb') as f:
        svm = pickle.load(f)


    ########################################### normal classification with SVM#######################

    y_pred = svm.predict(x)
    y_prob = svm.predict_proba(x)
    y_prob = y_prob[:,1]








