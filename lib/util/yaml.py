from os import path
import yaml

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
