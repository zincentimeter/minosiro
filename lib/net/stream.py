from pathlib import Path
import time
from urllib.parse import urlparse
import requests
import hashlib
import dateutil.parser
import calendar

import lib.file.file as file

def download(url : str, local_directory : Path,
             proxy_conf : dict[str,str] = None) -> tuple[
                 bool, file.Location, str, str, str]:

    download_request = requests.get(url=url, proxies=proxy_conf)
    sha256 = hashlib.sha256(download_request.content).hexdigest()
    file_name = f'{sha256[4:]}{Path(urlparse(url).path).suffix}'
    
    dir_abs = Path(local_directory, sha256[0:2], sha256[2:4])
    dir_abs.mkdir(parents=True, exist_ok=True)
    
    file_abs = file.Location(dir_abs, file_name)
    with file_abs.open(mode='wb') as file_handle:
        file_handle.write(download_request.content)
    
    print(f'DOWNLOADED: {Path(dir_abs, file_name)} .')
    
    content_type = download_request.headers.get('Content-Type', default=None)
    date_string = download_request.headers.get('Date', default=None)
    
    try:
        # time.mktime() only accepts local time, not utc!
        download_unix_timestamp = int(calendar.timegm(
            dateutil.parser.parse(date_string).utctimetuple()))
    except ValueError:
        download_unix_timestamp = int(time.time())

    return True, file_abs, sha256, content_type, str(download_unix_timestamp)