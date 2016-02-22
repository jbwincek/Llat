""" Utility functions for llat """
import json
import pycuber as pc


def load_algs(filename):
    """Accepts filename of json data, returns encoded object alg file follows the format:
        '{alg_name1: [possible alg 1, possible alg 2, ...],
          alg_name2: [...], ...}

        `filename` – name of the file to load algs from, with extension

        Will re-raise file not found errors"""
    try:
        with open(filename, 'r') as j:
            file_data = j.read()
    except FileNotFoundError as e:
        raise e  # if the file isn't found, pass it up.
    return json.loads(file_data)


def reverse_alg(alg):
    return pc.Formula(alg).reverse()

