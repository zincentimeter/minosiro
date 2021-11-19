from os import path
import yaml

# extract args from file
@staticmethod
def yaml_to_dict(yaml_path : path) -> dict[str, str]:
    with open(yaml_path, mode='r') as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.FullLoader)
        return config
