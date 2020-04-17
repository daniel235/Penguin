from statistics import mean, median
#from keras.models import model_from_json
from tensorflow.keras.models import model_from_json
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from enum import Enum
import numpy as np

def createInstance(kmer, raw_signal, type=None):
    #requirements for NN model
    #kmer/median/mean/max/min
    return [kmer, median(raw_signal), mean(raw_signal), max(raw_signal), min(raw_signal)]


def prepareNNModel():
    #load model
    json_file = open("./Models/NNmodel.json", 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    loaded_model = model_from_json(loaded_model_json)
    #load weights
    loaded_model.load_weights("./Models/model.h5")
    print("loaded model")
    loaded_model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])
    return loaded_model


def createEncoder(X):
    #A G C T
    le = LabelEncoder()          
    le.fit(X)
    X = le.transform(X)
    X = X.reshape(-1, 1)

    #onehot encode
    _, n_features = np.shape(X)
    enc = OneHotEncoder(handle_unknown='ignore',categories='auto')
    enc.fit(X)
    onehots = enc.transform(X).toarray()
    return onehots
    

def to_onehot(encoder, kmer):
    onehot = encoder.transform(kmer).toarray()
    return onehot
    


    
