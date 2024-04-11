import json
import platform
import os


def _get_key_suffix() -> str:
    if(platform.system() == 'Linux'):
        return '_linux'    
    else:
        return '_win'

def get_config_path() -> str:
    if(platform.system() == 'Linux'):
        return '/code/config.json'
    else:
        return 'config.json'

def get_resource_path() -> str:
    key = 'resource_folder' + _get_key_suffix()
    return _config[key]
        
def get_upload_path() -> str:
    key = "upload_folder" + _get_key_suffix()
    upload = _config[key]
    return get_resource_path() + upload
    
def get_segment_path() -> str:
    key = "segment_folder" + _get_key_suffix()
    segment = _config[key]
    return get_resource_path() + segment
    
def get_summary_path() -> str:
    key = "summary_folder" + _get_key_suffix()
    summary = _config[key]
    return get_resource_path() + summary

_config_json = open(get_config_path()).read()
_config = json.loads(_config_json)

if __name__ == "__main__":
    print('config path: ' + get_config_path())