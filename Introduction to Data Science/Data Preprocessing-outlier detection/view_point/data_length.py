from utils.constant import Constant
from utils.utility import (count_frequency, calculate_statistics, write_NG_detailed_report)


def check_length(data_col, threshold_length, csv_file_name=None):
    """
    The function checks the length of the data column, apply only for data of string type, not for digit type
    :param csv_file_name: base name of csv file name
    :param data_col: data column.
    :param threshold_length: threshold of the length function.
    :return: result ('OK', 'NA', 'NG'), summary information,
    outline_details (DataFrame contains values and indexes of outline).
    """
    # TODO: Write your code to check data length here
    length = []
    size = len(data_col)
    for data in data_col:
        if type(data) != str:
            return Constant.RESULT_NA, "/", {}
        else:
            length.append(len(data))
    frequency_lst, frequency_dict = count_frequency(length)
    # print(frequency_lst, frequency_dict)
    Lmean, Lstdev, _ = calculate_statistics(length)
    # print(Lmean, Lstdev)
    out_line_length = []
    out_line = {}
    result = Constant.RESULT_NA
    for frequency in frequency_lst:
        if (frequency/size >= threshold_length) and frequency/size < 1:
            result = Constant.RESULT_NG
        elif frequency/size == 1:  # <=> len(frequency_lst)=1
            result = Constant.RESULT_OK
    # Create a dicitonary of outline
    if result == Constant.RESULT_NG:
        max_frequency = max(frequency_lst)
        out_line_frequency_lst = [x for x in frequency_lst if x < max_frequency]
        # Get list of out_line length from out_line_frequency
        for out_line_frequency in out_line_frequency_lst:
            for length, frequency in frequency_dict.items():
                if out_line_frequency == frequency:
                    out_line_length.append(length)
        # Get index and value of outile_value in the original data
        for index, data in enumerate(data_col):
            if len(data) in out_line_length:
                out_line[index] = data
        if csv_file_name:
            # Create detailed report
            write_NG_detailed_report(csv_file_name, data_col.name, 'check_length', out_line)
    sum_info = str(round(Lmean, 5)) + '/' + str(round(Lstdev, 5))
    return result, sum_info, out_line



