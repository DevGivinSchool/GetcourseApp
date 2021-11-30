import json
import logging
from error_handling import error_handler as error_handler


def read_json_file(file_path):
    try:
        with open(file_path) as json_file:
            data = json.load(json_file)
    except Exception as err:
        error_handler(str(err), do_exit=True)
    return data


def write_json_file(data, file_path, pretty=False):
    try:
        with open(file_path, 'w') as json_file:
            if pretty:
                json.dump(data, json_file, indent=2, sort_keys=True)
            else:
                json.dump(data, json_file)
    except Exception as err:
        error_handler(str(err), do_exit=False)

