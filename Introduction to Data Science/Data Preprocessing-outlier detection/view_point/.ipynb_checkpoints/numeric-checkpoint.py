import pandas as pd
from utils.constant import Constant
from utils.utility import write_NG_detailed_report


def check_numeric(data_col, threshold, csv_file_name=None):
    """
    Check numeric
    :param data_col: one data column from file csv.
    :param threshold: the point at which you start evaluate the result is NG,NA or OK.
    :return: result (OK, NG, NA), k (numbers of numeric rows), N (total values), summary information,
    abnormal_data_details (DataFrame contains values and indexes of invalid numeric).
    :param csv_file_name: base name of csv file name
     """

    # TODO: Write code to check numerical view point
    N = len(data_col)
    if N == 0:
        return Constant.RESULT_NA, 0, 0, "0/0", {}
    k = 0
    error_value = {}
    out_line = {}
    result = None
    for index, value in enumerate(data_col):
        try:
            if type(float(value)) == float:
                k += 1
        except ValueError:
            error_value[index] = value
    rate = k/N
    if rate < threshold:
        result = Constant.RESULT_NA
    elif (rate >= threshold) and (rate < 1):
        result = Constant.RESULT_NG
        out_line = error_value
        # Create detailed report
        if csv_file_name:
            write_NG_detailed_report(csv_file_name, data_col.name, 'check_numeric', out_line)
    elif rate == 1:
        result = Constant.RESULT_OK
    sum_info = str(k)+'/'+str(N)
    return result, k, N, sum_info, out_line




