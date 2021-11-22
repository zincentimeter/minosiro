import hashlib
import json

from pathlib import Path
from typing import IO

import lib.util.exception as exception

class FileError(exception.MetaException):
    pass

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

class BaseFile():
    def __init__(self, sha1 : str, location : Location = None,
                 **kwargs) -> None:
        self.location = Location(
            dir_abs=location.dir_abs,
            file_name=location.file_name.file_name)
        self.sha1 = sha1
        pass

class StructureInfo(BaseFile):
    suffix = '.minosiro.json'
    empty_json = json.dumps(dict(), ensure_ascii=False)
    encoding = 'utf8'
    
    @staticmethod
    def json_bin_to_json(structure_info_json_bin : bytes = None) -> str:
        if structure_info_json_bin == None:
            return StructureInfo.empty_json
        structure_info_json = structure_info_json_bin.decode(StructureInfo.encoding)
        try:
            structure_info_dict = json.loads(structure_info_json)
        except ValueError:
            return StructureInfo.empty_json
        return structure_info_dict
    
    @staticmethod
    def dict_to_json(structure_info_dict : dict = None) -> str:
        if structure_info_dict == None:
            return StructureInfo.empty_json
        
        structure_info_json = json.dumps(structure_info_dict, ensure_ascii=False)
        
        if structure_info_json == 'null':
            return StructureInfo.empty_json
        else:
            return structure_info_json

    @staticmethod
    def dict_to_json_bin(structure_info_dict : dict = None) -> bytes:
        return StructureInfo.dict_to_json(structure_info_dict).encode(
            StructureInfo.encoding)

    def __init__(self, file_instance : File = None,  **kwargs) -> None:
        file_location = file_instance.location
        
        self.location = Location(
            dir_abs=file_location.dir_abs,
            file_name=file_location.file_name.file_stem + StructureInfo.suffix)

    def write(self, structure_info_content : bytes) -> bool:
        self.sha1 = hashlib.sha1(structure_info_content)
        with self.location.open(mode='wb') as file_handle:
            file_handle.write(structure_info_content)
        return True

    def write_dict(self, structure_info_dict : dict = None) -> bool:
        structure_info_content = StructureInfo.dict_to_json_bin(structure_info_dict)
        self.write(structure_info_content)
    
    def read_dict(self) -> dict:
        with self.location.open(mode='rb') as file_handle:
            read_dict_content = file_handle.read()
        return StructureInfo.json_bin_to_json(read_dict_content)
        
    def append_dict(self, structure_info_dict : dict = None) -> bool:
        if (structure_info_dict == None):
            print("Nothing to append. Aborted.")
            return False
        current_dict = self.read_dict()
        temp_dict = dict()
        temp_dict.update(current_dict)
        temp_dict.update(structure_info_dict)
        return self.write_dict(temp_dict)

