from sklearn.metrics import r2_score, recall_score
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd
import numpy as np
import math
from collections import Counter


def predict(model, X_data, y_df):  

    y_pred = model.predict(X_data)
    result_df = y_df.copy()
    result_df['pred_speed'] = y_pred
    result_df = result_df.sort_values(['race_id', 'pred_speed'], ascending=[True, False])
    result_df = result_df.reset_index(drop=True)
    
    list_race_id = sorted(result_df['race_id'].unique())
    list_rank = np.array([])

    counter_race_id = Counter(result_df['race_id'])
    for race_id in list_race_id:
        num_horse = counter_race_id[race_id]
        rank = np.arange(1, num_horse+1, step=1, dtype=np.int64)
        list_rank = np.append(list_rank, rank)
    
    result_df['rank'] = list_rank
    result_df['rank'] = result_df['rank'].astype(int)
    result_df['top3_pred'] = 0
    result_df.loc[result_df['rank']<=3, 'top3_pred'] = 1
        
    rate = recall_score(result_df['top3'], result_df['top3_pred'])
    r2 = r2_score(result_df['speed'], result_df['pred_speed'])
    mae = mean_absolute_error(result_df['speed'], result_df['pred_speed'])
    mse = mean_squared_error(result_df['speed'], result_df['pred_speed'])
    rmse = math.sqrt(mse)
    
    return rate, r2, mae, rmse, result_df


def predict_new_race(model, new_race_folder_path):  

    test_data = create_test_data(new_race_folder_path)
    X_test = test_data.drop('KettoNum', axis=1)
    X_test = transform_data(X_test)
    y_pred = model.predict(X_test)
    # process result
    result_df = test_data[['KettoNum', 'Umaban']]
    result_df['y_pred'] = y_pred
    result_df.sort_values(by='y_pred', ascending=False, inplace=True)

    result_df['rank'] = np.arange(1, len(result_df)+1, step=1)
    result_df.drop('y_pred', axis=1, inplace=True)
    result_df.reset_index(drop=True, inplace=True)
    # Save result
    result_df.to_csv('result_df.csv', index=False)
    return result_df

def evaluate(model, X, y_df):
    rate, r2, mae, rmse, result_df = predict(model, X, y_df)
    print('Sai số rmse:                    %.3f'%rmse)
    print('Hệ số xác định r2-score: %.3f'%r2)
    print('Tỉ lệ True positive:           %.3f'%rate)
    return result_df
