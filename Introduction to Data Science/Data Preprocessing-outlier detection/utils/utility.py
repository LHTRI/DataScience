import os
import shutil
import pandas as pd
import numpy as np
from datetime import datetime
import csv
import chardet
from collections import Counter
import logging
from utils.constant import ErrorMessage


def find_csv_file_names(input_folder, suffix=".csv"):
    """
    Find csv name
    :param input_folder: Folder path
    :param suffix: suffix
    :return: name of csv file
    """
    file_names = os.listdir(input_folder)
    return [filename for filename in file_names if filename.endswith(suffix)]


def find_file_name_err(input_folder, suffix=".csv"):
    """
    Find file name error
    :param input_folder: Folder path
    :param suffix: suffix
    :return: file name is not csv
    """
    file_names = os.listdir(input_folder)
    error_file_name_list = []
    for file_name in file_names:
        if file_name.endswith(suffix):
            pass
        else:
            error_file_name_list.append(file_name)
            logging.info(ErrorMessage.ERROR__FILE_WRONG_FORMAT.format(file_name))
    return error_file_name_list


def write_error_file(error_file_name, output_dir):
    """
    Write error file
    :param error_file_name: name of file is not csv
    :param output_dir: Path to the output directory
    :return: None
    """
    df = pd.DataFrame({'Error_file': error_file_name})
    df.to_csv(output_dir, mode='w', index=False)


#######################################################
# TODO: Write your common functions here
#######################################################

def get_file_encoding(file_path):
    # Check encoding of each row
    encoding_list = []
    with open(file_path, 'rb') as f:
        reader = f.readlines()
        for idx, row in enumerate(reader):
            row_encoding_dict = chardet.detect(row)
            row_encoding = row_encoding_dict['encoding']
            if row_encoding is None:
                logging.warning('The format of {} is incorrect, encoding of row {} undefined'.format(file_path, idx+1))
            else:
                encoding_list.append(row_encoding)
    encoding_categories = Counter(encoding_list)
    if len(encoding_categories) == 1:
        logging.info("The encoding of file '{}' is '{}'.".format(file_path, row_encoding))
        return row_encoding
    else:
        return None


def validate_csv_file(file_path):
    flag = True
    # Read file data
    rows = []
    with open(file_path, 'rt', newline='', encoding="utf8") as f:
        reader = csv.reader(f, strict=True)
        try:
            for row in reader:
                rows.append(row)
                # print(row)
        except UnicodeDecodeError as e:
            logging.error("The format of file '{}' is incorrect -> UnicodeDecodeError: {}".format(file_path, e))
            flag = False
        except csv.Error as e:
            logging.error('The format of file "{}" is incorrect -> line {}: {}.'.format(file_path, reader.line_num, e))
            flag = False
        except EnvironmentError as e:
            logging.error('System error: {}.'.format(e))
        except Exception as e:
            logging.exception('Exception: {}.'.format(e))
        else:
            pass
    if len(rows) == 1:
        logging.warning("Fields of file '{}' have not data.".format(file_path))
        flag = False
    # Check length of each row if row number >= 2
    elif len(rows) >= 2:
        name_of_fields = rows[0]
        number_of_fields = len(name_of_fields)
        for index, row in enumerate(rows[1:]):
            if len(row) != number_of_fields:
                logging.warning("The length of row {} in file '{}' is incorrect".format(index+1, file_path))
                flag = False
        # Check valid of column name
        for name in name_of_fields:
            if " " in name:
                logging.warning("It has white space in field '{}' ".format(name))
                flag = False
    if not flag:
        return False
    else:
        return True


def count_frequency(lst):
    my_lst = lst.copy()
    my_set = set(my_lst)
    # Create a dictionary of frequency with format {'key':frequency,} where key is in my_set
    frequency_dict = {}
    frequency_lst = []
    for key in my_set:
        frequency = 0
        for x in my_lst:
            if x == key:
                # Count occurrence of value x
                frequency += 1
        frequency_dict[key] = frequency
        frequency_lst.append(frequency)
    return frequency_lst, frequency_dict


def calculate_statistics(lst):
    size = len(lst)
    if size == 0 or size == 1:
        return None, None, None
    mean = sum(lst)/size
    sum_square = sum([(x-mean)*(x-mean) for x in lst])
    stdev = (sum_square/(size-1))**0.5
    if stdev == 0:
        z_score_list = [0 for x in lst]
    else:
        z_score_list = [(x-mean)/stdev for x in lst]
    return mean, stdev, z_score_list


def find_median(lst):
    size = len(lst)
    if size == 1:
        return lst[0]
    if len(lst) % 2 == 0:
        median = (lst[int(size/2)-1] + lst[int(size/2)])/2
    else:
        median = lst[int(size/2)]
    return median


def calculate_quartile(lst):
    data = lst.copy()
    size = len(data)
    if size == 0:
        return None, None, None, None
    elif size == 1:
        return data[0], data[0], data[0], 0
    data.sort()
    # Calculate median from all values of this data_col: Called Q2
    Q2 = find_median(data)
    # Calculate median of array of values that smaller than Q2. Called Q1
    first_half_list = data[:int(size / 2)]
    Q1 = find_median(first_half_list)
    # Calculate median of array of values that greater than Q2. Called Q3
    second_half_list = data[int((size + 1) / 2):]
    Q3 = find_median(second_half_list)
    IQR = Q3 - Q1
    return Q1, Q2, Q3, IQR


def write_check_result(check_results, column_name, output_dir):
    """
    Write check result to csv file
    :param column_name: name of column in input file
    :param check_results: results and summary information of checking viewpoints for each column
    :param output_dir: Path to the output directory
    :return: None
    """
    df = pd.DataFrame(check_results, columns=column_name)
    df.to_csv(output_dir, mode='w', index=False)


def write_NG_detailed_report(csv_file_name, column_name, viewpoint_name, out_line):
    # Get output_folder path
    output_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', "output\\error"))
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    file_base_name = "detectoutlier_NG_" + csv_file_name[:-4] + "_" + column_name \
                     + "_" + viewpoint_name + "_" + str(current_time) + ".csv"
    file_name = output_folder + '\\' + file_base_name
    column = ["row_index", "values"]
    # Convert out_line of dictionary to list
    out_line_list = []
    for key, value in out_line.items():
        temp = [key, value]
        out_line_list.append(temp)
    df = pd.DataFrame(out_line_list, columns=column)
    df.to_csv(file_name, mode='w', index=False)


def erase_old_files(output_folder):
    for filename in os.listdir(output_folder):
        file_path = os.path.join(output_folder, filename)
        try:
            # remove file
            if (os.path.isfile(file_path) or os.path.islink(file_path)) and "detectoutlier_NG" in filename:
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def check_data_type_column(csv_file_name, data):
    data_type_list = []
    for column in data.columns:
        """
        if data[column].dtype == np.float64 or data[column].dtype == np.int64:
            data_type = "numeric"
        else:
            data_type = "str"
        """
        # print(data[column].dtype)
        data_type_list.append([column, data[column].dtype])
    # Write info to a csv file
    # Get output_folder path
    output_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', "output"))
    file_name = output_folder + '\\' + csv_file_name[:-4] + "_column_data_type.csv"
    column = ["column_name", "data_type"]
    df = pd.DataFrame(data_type_list, columns=column)
    df.to_csv(file_name, mode='w', index=False)

