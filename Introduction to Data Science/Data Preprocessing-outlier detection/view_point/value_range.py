import pandas as pd
from utils.constant import Constant
from utils.utility import (calculate_statistics, calculate_quartile, write_NG_detailed_report)


def check_value_range(data_col, threshold_range_z_score, threshold_range_iqr, csv_file_name=None):
    """
    The function checks value range of the data column, apply only for data of digit type
    :param csv_file_name: base name of csv file name
    :param data_col: one data column from file csv.
    :param threshold_range_z_score: threshold_z_score of the length function
    :param threshold_range_iqr: threshold_z_iqr of the length function
    :return: result ('OK', 'NA', 'NG'), summary information,
    outline_details (DataFrame contains values and indexes of outline).
    """

    # TODO: write your code here
    # Check if value is str
    for data in data_col:
        if type(data) == str or pd.isnull(data):
            return Constant.RESULT_NA, "/", {}
    if len(data_col) == 0:
        return Constant.RESULT_NA, "/", {}
    elif len(data_col) == 1:
        return Constant.RESULT_OK, "{}/0".format(data_col[0]), {}
    # Calculate IQR
    data = list(data_col)
    Q1, Q2, Q3, IQR = calculate_quartile(data)
    # Calculate [Low, Up] value based on threshold_iqr:
    low = Q1-threshold_range_iqr*IQR
    # print(low,'low')
    up = Q3+threshold_range_iqr*IQR
    # Calculate mean of all values in column: mean
    Vmean, Vstdev, z_score_list = calculate_statistics(data)
    # print(Vmean, Vstdev, z_score_list)
    out_line = {}
    for index, x in enumerate(data_col):
        if (x < low) or (x > up) or (abs(z_score_list[index]) > threshold_range_z_score):
            out_line[index] = x
    if len(out_line) == 0:
        result = Constant.RESULT_OK
    else:
        result = Constant.RESULT_NG
        # Create detailed report
        if csv_file_name:
            write_NG_detailed_report(csv_file_name, data_col.name, 'check_value_range', out_line)
    sum_info = str(round(Vmean, 5)) + '/' + str(round(Vstdev, 5))
    return result, sum_info, out_line




