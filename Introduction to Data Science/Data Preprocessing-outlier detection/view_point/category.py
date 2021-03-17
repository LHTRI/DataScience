from utils.constant import Constant
from utils.utility import (count_frequency, calculate_statistics, write_NG_detailed_report)


def check_category(data_col, threshold_category, csv_file_name=None):
    """
    The function checks category of the data column
    :param csv_file_name: base name of csv file name
    :param data_col:  one data column from file csv.
    :param threshold_category: threshold of the length function.
    :return: result ('OK', 'NA', 'NG'), summary information,
    outline_details (DataFrame contains values and indexes of outline).
    """
    # TODO: write your code to check category column here
    # Counter frequency of each unique value in data_col and store in a dictionary
    data = list(data_col)
    if len(data) == 0:
        return Constant.RESULT_NA, "/", {}
    elif len(data) == 1:
        return Constant.RESULT_OK, "/", {}
    frequency_lst, frequency_dict = count_frequency(data)
    frequency_mean, frequency_stdev, z_score_list = calculate_statistics(frequency_lst)
    out_line_frequency = []
    out_line_value = []
    out_line = {}
    for index, z_score in enumerate(z_score_list):
        if z_score < -threshold_category:
            out_line_frequency.append(frequency_lst[index])
    if len(out_line_frequency) == 0:
        result = Constant.RESULT_OK
    else:
        result = Constant.RESULT_NG
        # Get key by frequency value from frequency_dict
        for out_ln in out_line_frequency:
            for key, value in frequency_dict.items():
                if out_ln == value:
                    out_line_value.append(key)
        # Get index of outile_value in the original data
        for index, value in enumerate(data):
            if value in out_line_value:
                out_line[index] = value
        # Create detailed report
        if csv_file_name:
            write_NG_detailed_report(csv_file_name, data_col.name, 'check_category', out_line)
    sum_info = str(round(frequency_mean, 5)) + '/' + str(round(frequency_stdev, 5))
    return result, sum_info, out_line


