import sys
import os.path as path
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import joblib
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from common import transform_new_race_data as trans, create_new_race_data as cr
import warnings
warnings.filterwarnings("ignore") 

def my_r2_score(y_true, y_pred):
    SS_res =  K.sum(K.square(y_true - y_pred)) 
    SS_tot = K.sum(K.square(y_true - K.mean(y_true) ) ) 
    return (1 - SS_res/(SS_tot + K.epsilon()) )


if __name__ == '__main__':

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
    model_path =  path.abspath(path.join("..\\processes\\model and improve"))
    #print(model_path)
    HR_MODEL = load_model(model_path+'\\best_model.hdf5', custom_objects={'my_r2_score': my_r2_score})
    # Load train_data
    train_data = pd.read_csv('..\\processes\\model and improve\\train_data_best.csv')

    data_folder_path = path.abspath(path.join('' ,"../data//new_race_data"))
    #print('data_folder_path', data_folder_path)
    # Create new race data
    test_data = cr.create_new_race_data(data_folder_path)
    # Transform new race data
    X_test = trans.transform_new_race_data(train_data, test_data)
    y_pred = HR_MODEL.predict(X_test)
    #print(y_pred)
    result_df = test_data[['KettoNum', 'Umaban']]
    result_df['speed_pred'] = y_pred
    result_df.sort_values(by='speed_pred', ascending=False, inplace=True)

    result_df['rank'] = np.arange(1, len(result_df)+1, step=1)
    #result_df.drop('speed_pred', axis=1, inplace=True)
    result_df.reset_index(drop=True, inplace=True)
    print(result_df)
    # Save result
    result_df.to_csv('result_df.csv', index=False)
