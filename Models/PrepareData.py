from statistics import mean, median
#from keras.models import model_from_json
from tensorflow.keras.models import model_from_json


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