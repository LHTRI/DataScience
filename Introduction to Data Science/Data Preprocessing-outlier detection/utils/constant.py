###############################################

# TODO: Define your constant values here

###############################################


class Constant(object):
    SUMMARY_OUTPUT_FILENAME = "summary_report.csv"
    THRESHOLD = 'threshold'
    EMAIL_DEF = 'format_email'
    THRESHOLD_IQR = 'threshold_iqr'
    THRESHOLD_ZSCORE = 'threshold_zscore'
    RESULT_OK = 'OK'
    RESULT_NA = 'NA'
    RESULT_NG = 'NG'

    COLUMN_SKIP = 2

    INDEX = 'index'
    VALUE = 'value'
    LENGTH = 'length'
    Z_SCORE = 'z_score'
    IS_OUTLIER = 'is_outlier'
    SORT = 'sort'


class ErrorMessage(object):
    ERROR_NOT_FOUND = " Error: Can not find {0} in configuration file."
    ERROR_NOT_EXIST = "Error: {0} does not exist."
    ERROR_COLUMN_NOT_EXIST = " Error: File {0}, column {1} does not exist."
    ERROR_THRESHOLD_MISSING_VALUE = "Error: In the configuration file, the threshold {0} is a missing value."
    ERROR_MISSING_VALUE = " Error: {0} is missing value in configuration file."
    ERROR_WRONG_FORMAT = " Error: The format of {0} in the configuration file is incorrect."
    ERROR_NULL = " Error: File {0} is null."
    ERROR_ENCODING = "Error: File {0}, column {1} is invalid encoding."
    ERROR_NOT_FOUND_VALUE = " Error: {0} is not found in configuration file."
    ERROR__FILE_WRONG_FORMAT = " Error: The format of {0} is incorrect."
    ERROR_THRESHOLD_WRONG_VALUE = "Error: Threshold {0} is not a valid value."


class ListThreshold(object):
    CHECK_NUMERIC = 'check_numeric'
    CHECK_CATEGORY = 'check_category'
    CHECK_LENGTH = 'check_length'
    CHECK_VALUE_RANGE = 'check_value_range'
    THRESHOLD_ZSCORE = 'threshold_zscore'
    THRESHOLD_IQR = 'threshold_iqr'


class Config(object):
    CONFIG_FOLDER = '\config'
    CONFIG_FILENAME = '\DetectOutlier.yml'
