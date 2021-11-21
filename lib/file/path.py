import pathlib
def get_type_path(file_type : str, rabbit_hole : str,
                  **dir_conf : dict[str, str]) -> pathlib.Path:
    return pathlib.Path(rabbit_hole, dir_conf['structure'][file_type])