# coding=utf-8
import os, sys
import configparser

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from FZStatistics.KDFZObject import KDFZObject
from FZStatistics.KDFocalZonalStats import KDFocalZonalStats


def convert_value(value, target_type, default=None):
    if value == "None":
        return default
    try:
        return target_type(value)
    except ValueError:
        return default


def validate_path(path, check_directory=False):
    if not path:
        return False, "Error: Path is empty.\n"

    if check_directory:
        if os.path.isdir(path):
            return True, f"Directory exists: {path}\n"
        else:
            return False, f"Directory does not exist: {path}\n"
    else:
        if os.path.isfile(path):
            return True, f"File exists: {path}\n"
        else:
            return False, f"File does not exist: {path}\n"


def check_string_type(s):
    if s == "":
        return 'empty'

    try:
        int(s)
        return 'int'
    except ValueError:
        try:
            float(s)
            return 'float'
        except ValueError:
            return 'str'


def check_variable(var_name, var_value_str, expected_type, allow_zero=False):
    var_type = check_string_type(var_value_str)
    if var_type == "int":
        var_value = int(var_value_str)
    elif var_type == "float":
        var_value = float(var_value_str)
    else:
        return False, f"{var_name}: Value is not a number\n"

    if expected_type not in ['int', 'float']:
        return False, f"{var_name}: expected type must be 'int' or 'float'\n"

    if var_value < 0:
        return False, f"{var_name}: Value must be greater than or equal to 0\n"

    if not allow_zero and var_value == 0:
        return False, f"{var_name}: Value cannot be 0\n"

    if expected_type == 'int':
        if isinstance(var_value, int):
            return True, var_value
        else:
            return False, f"{var_name}: Expected an integer but got a float\n"

    if expected_type == 'float':
        if isinstance(var_value, float):
            return True, var_value
        else:
            return True, float(var_value)


def check_percentile(percentile):
    try:
        percentile = float(percentile)
        if 0 < percentile <= 100:
            return True, percentile
        else:
            return False, "Percentile: invalid\n"
    except ValueError:
        return False, "Percentile: invalid\n"


def read_config(file_name):
    # Check if the file exists
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"Configuration file '{file_name}' does not exist")

    # Create ConfigParser object
    config = configparser.ConfigParser()

    try:
        # Read the configuration file
        config.read(file_name)

        # Check if the configuration file is empty
        if not config.sections():
            raise ValueError(f"Configuration file '{file_name}' is empty or improperly formatted")

        objects = []
        for section in config.sections():
            try:
                # <editor-fold desc="Read parameters from configuration">
                value_file_name = config[section].get('value_file_name', '')
                zone_file_name = config[section].get('zone_file_name', '')
                result_file_name = config[section].get('result_file_name', '')
                unit = config[section].get('unit', '')
                wnd_type = config[section].get('wnd_type', '')
                half_length = convert_value(config[section].get('half_length', 'None'), int)
                half_width = convert_value(config[section].get('half_width', 'None'), int)
                radius = convert_value(config[section].get('radius', 'None'), int)
                semi_majr_length = convert_value(config[section].get('semi_majr_length', 'None'), int)
                ratio = convert_value(config[section].get('ratio', 'None'), float)
                angle = convert_value(config[section].get('angle', 'None'), float)
                stats_type = config[section].get('stats_type', '')
                percentile = convert_value(config[section].get('percentile', 'None'), float)
                div_columns = convert_value(config[section].get('div_columns', 'None'), int)
                div_rows = convert_value(config[section].get('div_rows', 'None'), int)
                proc_nums = convert_value(config[section].get('proc_nums', 'None'), int)
                threshold = convert_value(config[section].get('threshold', 'None'), int)
                is_ign_nodata = config[section].get('is_ign_nodata', 'False') == 'True'
                stats_method = config[section].get('stats_method', '')
                # </editor-fold>

                # Create configuration object

                obj = KDFZObject(
                    value_file_name, zone_file_name, result_file_name,
                    unit, wnd_type, half_length, half_width, radius,
                    semi_majr_length, ratio, angle, stats_type, percentile,
                    div_columns, div_rows, proc_nums, threshold, is_ign_nodata,
                    stats_method
                )
                objects.append(obj)

            except KeyError as e:
                raise KeyError(f"Missing expected configuration item in section '{section}': {e}")
            except ValueError as e:
                raise ValueError(f"Invalid value in section '{section}': {e}")

        return objects

    except (configparser.Error, ValueError) as e:
        # Handle errors related to reading or formatting the configuration file
        raise RuntimeError(f"Failed to read configuration file '{file_name}': {e}")


def write_config(filename, object):
    config = configparser.ConfigParser()
    config.read(filename)

    if config.sections():
        last_section = config.sections()[-1]
        last_section_number = int(last_section.replace('Object', ''))
    else:
        last_section_number = 0

    section_name = f'Object{last_section_number + 1}'
    if not config.has_section(section_name):
        config.add_section(section_name)

    # <editor-fold desc="Set parameters from configuration">
    config.set(section_name, 'value_file_name', str(object.value_file_name))
    config.set(section_name, 'zone_file_name', str(object.zone_file_name))
    config.set(section_name, 'result_file_name', str(object.result_file_name))
    config.set(section_name, 'unit', str(object.unit))
    config.set(section_name, 'wnd_type', str(object.wnd_type))
    config.set(section_name, 'half_length', str(object.half_length))
    config.set(section_name, 'half_width', str(object.half_width))
    config.set(section_name, 'radius', str(object.radius))
    config.set(section_name, 'semi_majr_length', str(object.semi_majr_length))
    config.set(section_name, 'ratio', str(object.ratio))
    config.set(section_name, 'angle', str(object.angle))
    config.set(section_name, 'stats_type', str(object.stats_type))
    config.set(section_name, 'percentile', str(object.percentile))
    config.set(section_name, 'div_columns', str(object.div_columns))
    config.set(section_name, 'div_rows', str(object.div_rows))
    config.set(section_name, 'proc_nums', str(object.proc_nums))
    config.set(section_name, 'threshold', str(object.threshold))
    config.set(section_name, 'is_ign_nodata', str(object.is_ign_nodata))
    config.set(section_name, 'stats_method', str(object.stats_method))
    # </editor-fold>

    # Write updated config to file
    with open(filename, 'w') as configfile:
        config.write(configfile)


def run_config(file_name):
    objects = read_config(file_name)

    i = 1
    for object in objects:
        print("Processing %d ..." % (i))
        stats = KDFocalZonalStats(object)
        stats.process()
        i = i + 1


def process_object(object):
    stats = KDFocalZonalStats(object)
    stats.process()
