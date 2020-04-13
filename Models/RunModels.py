from keras.models import model_from_json

def run_nn(model, instance):
    model.predict(instance)
