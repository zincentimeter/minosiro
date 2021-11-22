from typing import Literal
import re

def get_matched_str(pattern : Literal, string : str) -> str:
    match = re.search(pattern=pattern, string=string)
    if (match == None):
        return None
    return match[0]

def get_pattern_removed(pattern : Literal, string : str) -> str:
    if (string == None):
        return None
    return re.sub(pattern=pattern, repl='', string=string)

def debracket(string : str) -> str:
    return get_pattern_removed(
        pattern=r"{|}",
        string=get_matched_str(pattern=r"\{(.*?)\}", string=string))