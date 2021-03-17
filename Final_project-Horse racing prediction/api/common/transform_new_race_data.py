import joblib
import json
import pandas as pd
import numpy as np

def transform_new_race_data(train_data, test_data):
    
    # Lấy dữ liệu cho các new col target encoding
    for code_col, value_col in zip(['ChokyosiCode', 'BanusiCode', 'UM_BreederCode'], ['top2_ChokyosiCode', 'top2_BanusiCode', 'top2_UM_BreederCode']):
        test_data[value_col] = 0
        for code in test_data[code_col]:
            try:
                value = train_data[train_data[code_col]==code][value_col].tolist()[0]
            except IndexError:
                value = 0
            test_data.loc[test_data[code_col]==code, value_col] = value
            
     # Lấy dữ liệu cho before_Odds
    mean_Odds = train_data['Odds'].mean()
    for KettoNum in test_data['KettoNum']:
        try:
            last_KettoNum_Odds = train_data[train_data['KettoNum']==KettoNum][['race_id', 'Odds']].sort_values(by='race_id')['Odds'].tolist()[-1]
        except IndexError:
            last_KettoNum_Odds = mean_Odds
        test_data.loc[test_data['KettoNum']==KettoNum, 'before_Odds'] = last_KettoNum_Odds       
    
    import joblib 
    enc = joblib.load('..\\processes\\model_and_improve\\enc.bin')
    scaler = joblib.load('..\\processes\\model_and_improve\\scaler.bin')
    
    import json
    with open('..\\processes\\model_and_improve\\feature_dict_all.json') as js:
        feature_dict = json.load(js)
    cat_col = feature_dict['cat_col']
    num_col = feature_dict['num_col']
    new_col = feature_dict['new_col']
    ref_col = feature_dict['ref_col'] # ['ChokyosiCode', 'BanusiCode', 'UM_BreederCode', 'Odds']
    
    cat_feature_names = enc.get_feature_names(cat_col)
    X_test_cat = test_data[cat_col]
    X_test_cat = enc.transform(X_test_cat).toarray()
    X_test_cat = pd.DataFrame(X_test_cat, columns=cat_feature_names)
    new_num_col = num_col + new_col
    X_test_num = test_data[new_num_col]
    X_scale = scaler.transform(X_test_num)
    X_test_num = pd.DataFrame(X_scale, columns=new_num_col)
    X_test = pd.concat([X_test_cat, X_test_num], axis=1, sort=False)

    extract_feature = feature_dict['extract_feature']
    new_extract_feature = extract_feature + new_col
    X_test = X_test[new_extract_feature]
    
    # Thay giá trị target encoding 
    for col in ['top2_ChokyosiCode', 'top2_BanusiCode', 'top2_UM_BreederCode']:
        X_test[col] = test_data[col]
    
    return X_test