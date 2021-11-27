from pathlib import Path
from typing import IO

class FileName():
    
    def __init__(self, file_name : str) -> None:
        self.file_name = file_name
        self.file_stem = Path(file_name).stem
        self.suffix = Path(file_name).suffix
        self.suffixes = Path(file_name).suffixes

    def __str__(self) -> str:
        return self.file_stem + self.suffix

class Location():
    
    def __init__(self, dir_abs : str, file_name : str) -> None:
        self.dir_abs = dir_abs
        self.file_name = FileName(file_name)

    def __str__(self) -> str:
        return Path(self.dir_abs, self.file_name.__str__()).__str__()
    
    def __path__(self) -> Path:
        return Path.joinpath(self.dir_abs, self.file_name.__str__())
    
    def open(self, mode : str = 'wb') -> IO:
        return Path(self.__path__()).open(mode=mode)

    def exists(self) -> bool:
        return Path(self.__path__()).exists()

def get_type_path(file_type : str, rabbit_hole : str,
                  **dir_conf : dict[str, str]) -> Path:
    return Path(rabbit_hole, dir_conf['structure'][file_type])