from os import path
import yaml
import re

import lib.util.regex as regex

# extract args from file
def yaml_to_dict(yaml_string : str = None, yaml_path : path = None) -> dict:
    if (yaml_path != None):
        return yaml_file_to_dict(yaml_path = yaml_path)
    if (yaml_string != None):
        return yaml_str_to_dict(yaml_string = yaml_string)
    
def yaml_str_to_dict(yaml_string : str) -> dict:
    return yaml.load(yaml_string, Loader=yaml.FullLoader)

def yaml_file_to_dict(yaml_path : path) -> dict:
    with open(yaml_path, mode='r') as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.FullLoader)
        return config

def parse_info_dict(info_layout : dict, **kwargs):
    return ParseAction.iterate_dict(info_layout, kwargs)

class ParseAction:
    
    def act(layout_entry, src) -> dict:
        if (type(layout_entry) == str):
            return ParseAction.get_value(layout_entry, src)
        elif (type(layout_entry) == list):
            return ParseAction.iterate_list(layout_entry, src)
        elif (type(layout_entry) == dict):
            return ParseAction.iterate_dict(layout_entry, src)
    
    def iterate_list(layout_entry : list, src) -> dict:
        result = dict()
        for item in layout_entry:
            result.update(ParseAction.act(layout_entry=item, src=src))
        return result
    
    def get_value(layout_value : str, src) -> dict:
        if (type(src) == str):
            return(re.sub(pattern='{.*}', repl=src, string=layout_value))
        if (type(src) == dict):
            try:
                src_value = src[layout_value]
            except ValueError:
                print('Cannot find corresponding layout in src.')
                src_value = ''
            return(dict({layout_value:src_value}))
    
    def iterate_dict(layout_dict : dict, src) -> dict:
        result = dict()
        for key, value in layout_dict.items():
            result[key] = ParseAction.act(layout_entry=value, src=src[key])
            # substitute key to the word in the bracket in value.
            if (type(value) != str):
                continue
            new_key = regex.debracket(value)
            if (new_key == None):
                continue
            result[new_key] = result.pop(key)
        return result
