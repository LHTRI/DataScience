import sys
import os.path as path
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import joblib
import json
import numpy as np
import pandas as pd

import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
from common import transform_new_race_data as trans

import warnings
warnings.filterwarnings("ignore") 


def my_r2_score(y_true, y_pred):
    SS_res =  K.sum(K.square(y_true - y_pred)) 
    SS_tot = K.sum(K.square(y_true - K.mean(y_true) ) ) 
    return (1 - SS_res/(SS_tot + K.epsilon()) )

class helloWorld(Resource):
    def get(self):
        return 'Hello World!'

class Predict(Resource):

    @staticmethod
    def post():

        post_data = request.get_json()

        test_data = pd.DataFrame.from_dict(post_data['data'], orient='columns')
        X_test = trans.transform_new_race_data(train_data, test_data)
        y_pred = HR_MODEL.predict(X_test).tolist()
        y_pred = json.dumps(y_pred)
          
        return y_pred


# Release gpu memory
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)

# Load model
model_path =  path.abspath(path.join("..\\processes\\model_and_improve"))
#print(model_path)
HR_MODEL = load_model(model_path+'\\improved_model.hdf5', custom_objects={'my_r2_score': my_r2_score})
# Load train_data
train_data = pd.read_csv('..\\processes\\model_and_improve\\train_data_all.csv')

APP = Flask(__name__)
API = Api(APP)
API.add_resource(helloWorld, '/')
API.add_resource(Predict, '/predict')

if __name__ == '__main__':
    APP.run(debug=True, host='127.0.0.1', port=1080, threaded=True)