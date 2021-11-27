from __future__ import annotations
import hashlib
import json
import mimetypes
import time
from pathlib import Path

from lib.net.stream import download
from lib.file.path import Location
from lib.util.exception import MetaException

class FileError(MetaException):
    pass

class BaseFile():
    def __init__(self, sha256 : str, location : Location = None,
                 **kwargs) -> None:
        self.location = Location(
            dir_abs=location.dir_abs,
            file_name=location.file_name.file_name)
        self.sha256 = sha256
        pass

class StructureInfo(BaseFile):
    suffix = '.minosiro.json'
    empty_json = json.dumps(dict(), ensure_ascii=False)
    encoding = 'utf8'
    
    @staticmethod
    def json_bin_to_json(structure_info_json_bin : bytes = None) -> dict:
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
        self.sha256 = hashlib.sha256(structure_info_content)
        with self.location.open(mode='wb') as file_handle:
            file_handle.write(structure_info_content)
        return True

    def write_dict(self, structure_info_dict : dict = None) -> bool:
        structure_info_content = StructureInfo.dict_to_json_bin(structure_info_dict)
        self.write(structure_info_content)
    
    def read_dict(self) -> dict:
        if (not self.location.exists()):
            return dict()
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

class File(BaseFile):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.structure_info = StructureInfo(file_instance=self, **kwargs)

    def get_info_dict(self) -> dict:
        file_info_dict = dict()
        file_info_dict['sha256'] = self.sha256
        file_info_dict['path'] = self.location.__str__()
        return file_info_dict
        
    def write_structure_info(self, structure_info_dict : dict = None) -> bool:
        return self.structure_info.write_dict(structure_info_dict)

    def append_structure_info(self, field_name : str = None,
                              structure_info_dict : dict = None) -> bool:
        if field_name == None:
            return self.structure_info.append_dict(structure_info_dict)
        temp_dict = dict()
        temp_dict[field_name] = structure_info_dict
        return self.structure_info.append_dict(temp_dict)


    @staticmethod
    def create_by_downloading(url : str, local_directory : Path,
                 proxy_conf : dict[str,str] = None,
                 structure_info_dict : dict = None) -> File:
        
        dl_success, location, sha256, content_type, download_unix_timestamp = \
            download(url, local_directory, proxy_conf)
        if (not dl_success):
            raise FileError('Failed to download.')

        file_instance = File(sha256=sha256, location=location)

        if (structure_info_dict == None):
            structure_info_dict = dict()

        structure_info_dict['file'] = file_instance.get_info_dict()
        structure_info_dict['file'].update(content_type=content_type)
        structure_info_dict['file'].update(archived_time=download_unix_timestamp)
        
        file_instance.append_structure_info(
            structure_info_dict=structure_info_dict)
        return file_instance