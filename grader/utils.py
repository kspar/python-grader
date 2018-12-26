""" An utility module containing utility functions used by the grader module
    and some useful pre-test hooks.
"""
import json
import traceback
import re
import ast


def import_module(path, name=None):
    if name is None:
        name = path
    import importlib.machinery
    loader = importlib.machinery.SourceFileLoader(name, path)
    module = loader.load_module(name)
    return module


def is_function(value):
    try:
        return hasattr(value, '__call__')
    except:
        return False

def quote_text_block(text):
    return "\n   " + text.replace("\n", "\n   ")

## Function descriptions
def beautifyDescription(description):
    """ Converts docstring of a function to a test description
        by removing excess whitespace and joining the answer on one
        line """
    lines = (line.strip() for line in description.split('\n'))
    return " ".join(filter(lambda x: x, lines))


def setDescription(function, description):
    import grader
    old_description = grader.get_test_name(function)
    if old_description in grader.testcases:
        grader.testcases.remove(old_description)
    description = beautifyDescription(description)
    function.__doc__ = description
    grader.testcases.add(description, function)


## Json managing
def load_json(json_string):
    " Loads json_string into an dict "
    return json.loads(json_string)


def dump_json(ordered_dict):
    " Dumps the dict to a string, indented "
    return json.dumps(ordered_dict, indent=4)

def extract_numbers(s, allow_decimal_comma=True):
    result = []
    if allow_decimal_comma:
        rexp = """((?:\+|\-)?\d+(?:(?:\.|,)\d+)?)"""
    else:
        rexp = """((?:\+|\-)?\d+(?:\.\d+)?)"""
        
    for item in re.findall(rexp, s):
        try:
            result.append(int(item))
        except:
            try:
                result.append(float(item.replace(",", ".")))
            except:
                pass
    return result

def contains_number(num_list_or_str, x, allowed_error=0, allow_decimal_comma=True):
    if isinstance(num_list_or_str, str):
        nums = extract_numbers(num_list_or_str, allow_decimal_comma)
    else:
        nums = num_list_or_str
    
    for num in nums:
        if abs(num - x) <= allowed_error:
            return True
    
    return False

def get_error_message(exception):
    type_ = type(exception)
    return "{}: {}".format(type_.__name__, str(exception))


def get_traceback(exception):
    type_, value, tb = type(exception), exception, exception.__traceback__
    return "".join(traceback.format_exception(type_, value, tb))


def read_code(path):
    import tokenize
    # encoding-safe open
    with tokenize.open(path) as sourceFile:
        contents = sourceFile.read()
    return contents

def ast_contains_name(node, name):
    if isinstance(node, ast.Name) and node.id == name:
        return True
    
    for child in ast.iter_child_nodes(node):
        if ast_contains_name(child, name):
            return True

    return False

def ast_contains(node, node_type):
    if isinstance(node, node_type):
        return True
    
    for child in ast.iter_child_nodes(node):
        if ast_contains(child, node_type):
            return True

    return False
    