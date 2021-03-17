import numpy as np
import pandas as pd

# Xây dựng hàm target_encoding cho các cột nominal variable

def target_encoding(data_df, column='KettoNum', target='top2', m='all'):
    
    df_train = data_df[data_df['id$Year']<2018]
    if m == 'all':
        m = len(df_train)
    # Compute the target mean
    target_mean = df_train[target].mean()

    # Compute the number of values and the mean of each group
    agg = df_train.groupby(column)[target].agg(['count', 'mean'])
    counts = agg['count']
    means = agg['mean']

    # Compute the "smoothed" means
    smooth_probability = (counts * means + m * target_mean) / (counts + m)
    
    # Convert
    new_column_name = 'converted_' + column
    data_df[new_column_name] = data_df[column]
    data_df[new_column_name] = data_df[new_column_name].map(smooth_probability)
    #print(target_mean)
    # Điền các giá bị khuyết của năm 2018 bằng giá trị trung bình
    data_df[new_column_name] = data_df[new_column_name].replace(np.nan, target_mean)
    
    return data_df