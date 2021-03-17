# -*- coding: utf-8 -*-
# TODO: WRITE YOUR NAME HERE
# Lê Hữu Trí - trilhfx04825@funix.edu.vn - FX04825
###################################################

import argparse
import os
import pandas as pd
import yaml
import logging
import datetime
from utils.utility import (get_file_encoding, validate_csv_file, write_check_result, erase_old_files)


from view_point.numeric import check_numeric
from view_point.category import check_category
from view_point.data_length import check_length
from view_point.value_range import check_value_range

from utils.constant import (Constant, ErrorMessage, ListThreshold, Config)
from utils.utility import (find_csv_file_names, find_file_name_err, write_error_file)


DetectOutlier_check_path = os.path.dirname(os.path.realpath(__file__))

config_path = DetectOutlier_check_path + Config.CONFIG_FOLDER + Config.CONFIG_FILENAME


def read_config_file(config_file):
    """
    'Type' for argument parse - check file format.
    :param config_file: File's path.
    :return: None.
    """
    if not os.path.exists(config_file):
        # Argument parse uses the ArgumentTypeError to give a rejection message like:
        # Error: argument input: x does not exist.
        logging.error(ErrorMessage.ERROR_NOT_EXIST.format(config_file))
        raise argparse.ArgumentTypeError(ErrorMessage.ERROR_NOT_EXIST.format(config_file))

    with open(config_file, 'r') as stream:
        try:
            config = yaml.load(stream, Loader=yaml.FullLoader)
            return config
        except yaml.YAMLError:
            logging.error(ErrorMessage.ERROR_WRONG_FORMAT.format(config_file))
            raise argparse.ArgumentTypeError(ErrorMessage.ERROR_WRONG_FORMAT.format(config_file))
    return None


def check_folder_exist(folder_path):
    """
    check exists of folder path.
    :param folder_path: Folder path.
    :return: Folder path if it exists.
    """
    abs_path = os.path.abspath(folder_path)
    if not os.path.isdir(abs_path):
        # Argument parse uses the ArgumentTypeError to give a rejection message like:
        # Error: argument input: x does not exist.
        logging.error(ErrorMessage.ERROR_NOT_EXIST.format(abs_path))
        raise argparse.ArgumentTypeError(ErrorMessage.ERROR_NOT_EXIST.format(abs_path))
    return abs_path


def read_input(file_path):
    # Get encoding of csv file
    file_encoding = get_file_encoding(file_path)
    if not file_encoding:
        logging.warning("Unable to determine encoding of file '{}',"
                        " please check file's encoding again!".format(file_path))
        return None
    # Validate general content of csv file
    if validate_csv_file(file_path):
        # Read data
        data = pd.read_csv(file_path, encoding=file_encoding)
        return data
    else:
        return None


def check_view_points(config, input_folder, output_folder):
    """
    Main function that calls other functions to:
        1. Read input data
        2. Check view point
        3. Save result
    :param config:  threshold configuration.
    :param input_folder: input path.
    :param output_folder: output path.
    :return: result.
    """

    logging.info("Begin load data ...   ")

    ###########################################################################
    # TODO: Read all files in input_folder. Write your function and call here
    ###########################################################################

    # Find csv file name
    csv_file_names = find_csv_file_names(input_folder, suffix=".csv")
    # Find file name error
    error_file_name_list = find_file_name_err(input_folder, suffix=".csv")
    # Write error file
    output_dir = DetectOutlier_check_path + "\\output\\error\\error_file_name.csv"
    write_error_file(error_file_name_list, output_dir)
    # Check only file "DBDetectOutlier.csv"(csv_file_names[0])
    file_base_name = "DBDetectOutlier.csv"  # csv_file_names[0]
    input_file = input_folder + '\\' + file_base_name
    data = read_input(input_file)
    if data is None:
        logging.warning("Data not ready")
        return None

    ###########################################################################
    # TODO: Check all columns with each check function
    ###########################################################################
    # Get threshold values from config file
    threshold_numeric = config[Constant.THRESHOLD][ListThreshold.CHECK_NUMERIC]
    threshold_zscore = config[Constant.THRESHOLD][ListThreshold.THRESHOLD_ZSCORE]
    threshold_iqr = config[Constant.THRESHOLD][ListThreshold.THRESHOLD_IQR]
    threshold_category = config[Constant.THRESHOLD][ListThreshold.CHECK_CATEGORY]
    threshold_length = config[Constant.THRESHOLD][ListThreshold.CHECK_LENGTH]
    # Create a list to store results
    check_results_manager = []
    # Create a dictionary to store all check functions with its parameter
    check_views = {check_numeric: [threshold_numeric, ],
                   check_value_range: [threshold_zscore, threshold_iqr, ],
                   check_category: [threshold_category, ],
                   check_length: [threshold_length, ]}

    # Erase all old files before writing NG detailed report
    error_folder = DetectOutlier_check_path + "\\output\\error"
    erase_old_files(error_folder)

    logging.info("Begin check files and writing NG detailed report...   ")

    for column in data.columns:
        for function, parameter in check_views.items():
            result = function(data[column], *parameter, file_base_name)
            if function == check_numeric:
                check_results_manager.append([file_base_name, column,
                                              function.__name__, result[0], result[3], result[4]])
            else:
                check_results_manager.append([file_base_name, column, function.__name__, *result])

    ###########################################################################
    # TODO: Call function to save the output
    ###########################################################################
    column_name = ["file_name", "column_name", "view_point", "result", "summary"]
    output_dir = output_folder + "\\Summary_detect_outlier.csv"
    sum_info = [x[:-1] for x in check_results_manager]  # skip outlier value in check_results
    write_check_result(sum_info, column_name, output_dir)

    return check_results_manager


def init():
    if not os.path.isdir(DetectOutlier_check_path + "\\logs"):
        os.makedirs(DetectOutlier_check_path + "\\logs")

    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    logging.basicConfig(
        handlers=[logging.FileHandler(DetectOutlier_check_path + '\\logs\\log_' + str(current_time) + '.log', 'w',),
                  logging.StreamHandler()],
        level=logging.INFO,
        format='%(asctime)2s - %(filename)s - %(funcName)s - %(lineno)s - %(levelname)s - %(msg)s')


def main():
    # call init function
    init()
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    """
    Command line options
    """
    parser._actions[0].help = 'Display the guidelines. Inputting paths are absolute or relative paths.'

    parser.add_argument(
        '-i',
        type=check_folder_exist,
        required=True,
        dest="directory",
        help='Path to the directory that contains the CSV file to check'
    )

    parser.add_argument(
        '-o',
        type=check_folder_exist,
        required=True,
        dest="output_folder",
        help=' Path to summary report'
    )

    parser.add_argument(
        '-c',
        type=read_config_file,
        default=config_path,  # Path of the config file.
        dest="config",
        help=' Path to configuration file'
    )

    logging.info('Parsing arguments ...')

    flags = parser.parse_args()

    # Call main function
    check_view_points(flags.config, flags.directory, flags.output_folder)

    print(' Done.')


if __name__ == '__main__':
    main()
