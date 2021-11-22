from pathlib import Path
from urllib.parse import urlparse
import requests
import hashlib

import lib.file.file as file

def download(url : str, local_directory : Path,
             proxy_conf : dict[str,str] = None) -> tuple[bool, file.Location, str]:

    download_request = requests.get(url=url, proxies=proxy_conf)
    
    sha1 = hashlib.sha1(download_request.content).hexdigest()
    file_name = f'{sha1[4:]}{Path(urlparse(url).path).suffix}'
    
    dir_abs = Path(local_directory, sha1[0:2], sha1[2:4])
    dir_abs.mkdir(parents=True, exist_ok=True)
    
    file_abs = file.Location(dir_abs, file_name)
    with file_abs.open(mode='wb') as file_handle:
        file_handle.write(download_request.content)
    
    print(f'DOWNLOADED: {Path(dir_abs, file_name)} .')
    
    return True, file_abs, sha1