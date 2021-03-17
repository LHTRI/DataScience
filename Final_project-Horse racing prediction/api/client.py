import sys
import os
import json
import requests
import pandas as pd
import numpy as np
import logging
import argparse
import os.path as path
from common import create_new_race_data as cr
import warnings
warnings.filterwarnings("ignore") 

url = 'http://127.0.0.1:1080/predict'  # localhost and the defined port + endpoint

if __name__ == '__main__':

    data_folder_path = path.abspath(path.join('' ,"../data//new_race_data"))
    #print('data_folder_path', data_folder_path)

    test_data = cr.create_new_race_data(data_folder_path)
    post_data = test_data.to_dict(orient='list')
    # send data
    post_data = {'data': post_data}
    response = requests.post(url, json=post_data)
    # get result
    y_pred = response.json() 
    y_pred = json.loads(y_pred)
    y_pred = np.asarray(y_pred)
    # process result
    result_df = test_data[['KettoNum', 'Umaban']]
    result_df['speed_pred'] = y_pred
    result_df.sort_values(by='speed_pred', ascending=False, inplace=True)

    result_df['rank'] = np.arange(1, len(result_df)+1, step=1)
    #result_df.drop('speed_pred', axis=1, inplace=True)
    result_df.reset_index(drop=True, inplace=True)
    print(result_df)
    # Save result
    result_df.to_csv('result_df.csv', index=False)
    
