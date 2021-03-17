import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_transformer
from sklearn.utils import shuffle
import joblib

def transform_split_data(data_df, id_col, cat_col, num_col, scale_data=False, target='speed', drop=None, shuffle=True, ref_col=None):
    
    # split train and test data
    train_data = data_df[data_df['Year']<2018]
    test_data = data_df[data_df['Year']==2018].reset_index() # for pd.concat
    id_train = data_df[data_df['Year']<2018][id_col]
    id_test = data_df[data_df['Year']==2018][id_col].reset_index(drop=True) # for pd.concat

    if ref_col:
        ref_train = data_df[data_df['Year']<2018][ref_col]
        ref_test = data_df[data_df['Year']==2018][ref_col].reset_index(drop=True) # for pd.concat
    else:
        ref_train = None
        ref_test = None

    # Create cat data
    X_train_cat = train_data[cat_col]
    X_test_cat = test_data[cat_col]
    
    enc = OneHotEncoder(drop=drop, handle_unknown='ignore')
    X_train_cat = enc.fit_transform(X_train_cat).toarray()
    X_test_cat = enc.transform(X_test_cat).toarray()
    
    cat_feature_names = enc.get_feature_names(cat_col)
    X_train_cat = pd.DataFrame(X_train_cat, columns=cat_feature_names)
    X_test_cat = pd.DataFrame(X_test_cat, columns=cat_feature_names)
    
    # Create num data
    X_train_num = train_data[num_col]
    X_test_num = test_data[num_col]
   
    if scale_data:
        scaler = StandardScaler()
        columns = X_train_num.columns
        X_scale = scaler.fit_transform(X_train_num)
        X_train_num = pd.DataFrame(X_scale, columns=columns)
        X_scale = scaler.transform(X_test_num)
        X_test_num = pd.DataFrame(X_scale, columns=columns)
        

    # Create X, y train
    X_train = pd.concat([X_train_cat, X_train_num], axis=1, sort=False)
    y_train_df = train_data[['id$Year', 'race_id', 'KettoNum', 'speed', 'Time', 'KakuteiJyuni', 'top3']]
        
    # Create X, y test
    X_test = pd.concat([X_test_cat, X_test_num], axis=1, sort=False)
    y_test_df = test_data[['id$Year', 'race_id', 'KettoNum', 'speed', 'Time', 'KakuteiJyuni', 'top3']]
    
    # shuffle train data
    if shuffle:
        if ref_train is None:
            df_train = pd.concat([X_train, y_train_df], axis=1, sort=False)
            drop_columns = y_train_df.columns.tolist()
        else:
            df_train = pd.concat([X_train, y_train_df, ref_train], axis=1, sort=False)
            drop_columns = y_train_df.columns.tolist() + ref_train.columns.tolist()
        
        df_train = df_train.sample(frac=1).reset_index(drop=True)
        X_train = df_train.drop(drop_columns, axis=1)
        y_train_df = df_train[['id$Year', 'race_id', 'KettoNum', 'speed', 'Time', 'KakuteiJyuni', 'top3']]
        id_train = df_train[id_col]
        if ref_col:
            ref_train = df_train[ref_col]
        #ref_

    # save enc and scale
    joblib.dump(enc, 'enc.bin')
    joblib.dump(scaler, 'scaler.bin')

    return X_train, y_train_df, X_test, y_test_df, id_train, id_test, ref_train, ref_test
