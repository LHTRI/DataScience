from scipy import stats
import numpy as np
import pandas as pd

def filter_outlier_value_range(dt, filter_columns = "all", threshold_zscore =3, threshold_iqr=1.5):

	data = dt.copy()
	
	if not isinstance(dt, pd.DataFrame):
		data = pd.DataFrame(dt, columns=['temp'])
		filter_columns = ['temp']
		
	if filter_columns == "all":
		filter_columns = data.columns
		filter_df = data
	else:
		filter_df = data[filter_columns]
		
	z = np.abs(stats.zscore(filter_df))
	filter_df = filter_df[(z < threshold_zscore).all(axis=1)]

	Q1 = filter_df.quantile(0.25)
	Q3 = filter_df.quantile(0.75)
	IQR = Q3 - Q1
	filter_df = filter_df[~((filter_df < (Q1 - threshold_iqr * IQR)) |(filter_df > (Q3 + threshold_iqr * IQR))).any(axis=1)]

	filtered_df = data
	filtered_df[filter_columns] = filter_df
	filtered_df = filtered_df.dropna()

	if not isinstance(dt, pd.DataFrame):
		return filtered_df['temp'].values
	else:
		return filtered_df


def filter_outlier_category(df, category_column=None, threshold_category =0.7):

    df_count = df.groupby(category_column, as_index=False).count()
    index  = np.where(df.columns != category_column)[0][0]
    column_name = df.columns[index]
    df_count = df_count.rename(columns={column_name:'count'})
    df_count = df_count[[category_column, 'count']]
    
    z = stats.zscore(df_count['count'])
    df_count['z'] = z
    df_count = df_count[df_count['z']>-threshold_category]
    
    df_category = pd.DataFrame(df_count[category_column])
    filtered_df = df.merge(df_category, on=category_column, how='right' )

    return filtered_df