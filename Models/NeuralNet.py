#to Get Reproducible Results with Keras #https://machinelearningmastery.com/reproducible-results-neural-networks-keras/

from numpy.random import seed

#seed(1)

import tensorflow
from numpy import loadtxt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense 
from tensorflow.keras.optimizers import SGD
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from sklearn.metrics import classification_report #for classifier evaluation
from sklearn.metrics import roc_auc_score # for printing AUC
#from sklearn.metrics import roc_auc_score # for printing AUC
from sklearn.metrics import roc_curve, auc

# To set seed random number
from numpy.random import seed

#tensorflow.random.set_seed(1234)
seed(1234)
####################################################

from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
import pandas as pd
from statistics import mean, median
import numpy as np
import sys
import Models.SignalPadding as signal
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler #For feature normalization

scaler = MinMaxScaler()

#get signal length:

def get_signal_length(x):  
    return len(x)


def get_df(c, m):
    dfControl = pd.read_csv(c, sep=' ', header=None)
    print(dfControl)
    dfModified = pd.read_csv(m, sep=' ', header=None)
    print(dfModified)
    return dfControl, dfModified

def run_neural_net(control, modified):
    #start pseudoExtractor 
    controlHela, pseudoHela = get_df(control, modified)

    #omit file name
    drp = [0, 2]
    controlHela = controlHela.drop(drp, axis=1) 
    pseudoHela = pseudoHela.drop(drp, axis=1)
    kmerData = []
    for i in range(len(controlHela)):
        kmer = controlHela.iloc[i, 0] 
        kmerData.append([kmer])

        values = controlHela.iloc[i, 1]  
        sig = ""
        for j in range(len(values)):
            if values[j] == '_':
                #convert to int
                kmerData[i].append(int(sig))
                sig = ""

            elif j == (len(values) - 1):
                sig += values[j]
                kmerData[i].append(int(sig))
                sig = ""

            else:
                sig += values[j]


    pseudoKmerData = []

    for i in range(len(pseudoHela)):
        kmer = pseudoHela.iloc[i, 0]
        pseudoKmerData.append([kmer])
        values = pseudoHela.iloc[i, 1]

        sig = ""
        for j in range(len(values)):
            if values[j] == '_':
                #convert to int
                pseudoKmerData[i].append(int(sig))
                sig = ""

            elif j == (len(values) - 1):
                sig += values[j]
                pseudoKmerData[i].append(int(sig))
                sig = ""

            else:
                sig += values[j]



    X = []
    Xval = []
    Y = []
    Yval = []


    prevIndexes = np.random.choice(len(controlHela), 360, replace=False)
    kmerData = np.array(kmerData)[prevIndexes]
    print("size of ", len(kmerData))
    total = 360 + len(pseudoHela)
    indexes = np.random.choice(total, total, replace=False)    


    for i in range(len(kmerData)):
        X.append(kmerData[i][0])


    for i in range(len(pseudoKmerData)):
        X.append(pseudoKmerData[i][0]) # Now X stores kmerData and pseudoKmerData


    #onehot encoding of kmer data
    le = preprocessing.LabelEncoder()          
    le.fit(X)
    print(le.classes_)
    X = le.transform(X)
    X = X.reshape(-1, 1)

    #onehot encode
    _, n_features = np.shape(X)
    print("&&&&&",n_features)
    enc = OneHotEncoder(handle_unknown='ignore',categories=[range(350)]*n_features)# note we replace n_values=350 which is depricated in vrsion 0.2 with categories=[range(350)]*n_features
    enc.fit(X)
    onehots = enc.transform(X).toarray()

    X = onehots


    ##feature extrextion from unmodified extracted Nanopore signal 
    allKmerData=[]
    for i in range(len(kmerData)):
        #orginal signal without padding
        allKmerData.append(kmerData[i][1:]) #store rows
        Xval.append([mean(kmerData[i][1:]), median(kmerData[i][1:]), max(kmerData[i][1:]), min(kmerData[i][1:]),get_signal_length(kmerData[i][1:])])
        Yval.append([0])



    ##feature extrextion from modified extracted Nanopore signal 
    for i in range(len(pseudoKmerData)):
        allKmerData.append(pseudoKmerData[i][1:])
        Xval.append([mean(pseudoKmerData[i][1:]), median(pseudoKmerData[i][1:]), max(pseudoKmerData[i][1:]), min(pseudoKmerData[i][1:]),get_signal_length(pseudoKmerData[i][1:])])
        Yval.append([1])




    #combine onehot encoding of kemer features with features extracted from nanopore signal
    for i in range(len(Xval)):
        for j in range(len(X[i])):
            Xval[i].append(X[i][j])


    #randomize indexes
    X = np.array(Xval)[indexes]                   
    #X = np.array(X)[indexes]    #when X has onehot encoding of kemer features only 
    Y = np.array(Yval)[indexes]
    print("pppppppppp",X.shape)
    print("jjjjjj",Y.shape)
    print("xxxxxxxxxxxxx",type(X))
    print("MMMMMMMMMMMMMMM",type(Y))
    print(len(X), len(Y))
    print("************************",X[0])
    print("-------------",Y[0])

    a,b=X.shape

    ########################################################

    #To get nanopore signal intenesity 
    #get padded signal data
    x= signal.signal_data(allKmerData)

    print("xxxxxxxxxxxxx",type(x))
    print(len(x))
    print("##########",x[0])

    #concatenate signal intensity features with other features extracted from extracted Nanopore signal
    X1=np.concatenate((X,x),axis=1)
    print("OOOOOOOOOOOOOOOOOO",X1)



    ####################################################define the NN model in keras##############################################



    # Evaluate the model: Model Accuracy, how often is the classifier correct

   
    # To set seed random number
    seed(4)

    tensorflow.random.set_seed(4)


    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
    #scale training data
    X_train= scaler.fit_transform(X_train) #https://stackoverflow.com/questions/41560021/numpy-ndarray-object-has-no-attribute-values
    #scale testing data
    X_test= scaler.fit_transform(X_test)

    model = Sequential()
    model.add(Dense(12, input_dim=b, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # compile the keras model
    #model.compile(loss='binary_crossentropy', optimizer=SGD(lr=0.05, momentum=0.99), metrics=['accuracy'])
    model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])

    # Fit the model                            #epochs= ﬁxed number of iterations through the dataset called epochs
    #model.fit(X_train, y_train, validation_split=0.2, epochs=150, batch_size=16) #batch_size=the number of instances that are evaluated before a weight update
    history=model.fit(X_train, y_train, validation_split=0.2, epochs=150, batch_size=len(X_train))

    # evaluate the keras model on the same dataset, but the dataset can be devided into training and testing, then fit the model on the training and evalaute the model on testing
    _, accuracy_train = model.evaluate(X_train, y_train, verbose=1)
    _, accuracy_test = model.evaluate(X_test, y_test, verbose=1)
    print('Accuracy on training: %.2f' % (accuracy_train*100))
    print('Accuracy on testing: %.2f' % (accuracy_test*100))

    #needed for plotting learning curve
    train_loss = history.history['loss']
    val_loss   = history.history['val_loss']
    train_acc  = history.history['accuracy']
    val_acc    = history.history['val_accuracy']
    xc         = range(50)

    #plot epochs versus accuracy curve.
    plt.plot(train_acc, label="Training accuracy")
    plt.plot(val_acc, label="Validation accuracy")
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend(loc="best")

    plt.show()

    # make class predictions with the model

    predictions = model.predict_classes(X_test)
    y_pred = model.predict_classes(X_test)
    y_prob = model.predict_proba(X_test)
    #y_prob = y_prob[:,1]

    print(classification_report(y_test, y_pred))
    auc=roc_auc_score(y_test.round(),y_pred)
    auc = float("{0:.3f}".format(auc))
    print("AUC=",auc)

    print("X 4Features+length before that was X1 features for 4 types of X featured concatenated with x")

    fpr, tpr, thresholds = metrics.roc_curve(y_test, y_prob)
    # Print ROC curve
    plt.plot(fpr,tpr)