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

def get_benchmark_data_path() -> str:
    return

def get_resource_path() -> str:
    key = 'resource_folder' + _get_key_suffix()
    return _tasks[key]
        
def get_upload_path() -> str:
    key = "upload_folder" + _get_key_suffix()
    upload = _tasks[key]
    return get_resource_path() + upload
    
def get_segment_path() -> str:
    key = "segment_folder" + _get_key_suffix()
    segment = _tasks[key]
    return get_resource_path() + segment

def get_segment_json_path() -> str:
    key = "segment_json_folder" + _get_key_suffix()
    segment_json = _tasks[key]
    return get_resource_path() + segment_json
    
def get_summary_path() -> str:
    key = "summary_folder" + _get_key_suffix()
    summary = _tasks[key]
    return get_resource_path() + summary

def get_broker_url() -> str:
    key = "broker_url"
    return _tasks[key]

def get_result_backend() -> str:
    key = "result_backend"
    return _tasks[key]

def get_util_path() -> str:
    return get_resource_path() + _tasks["util_folder" + _get_key_suffix()]

_tasks_json = open(get_config_path()).read()
_tasks = json.loads(_tasks_json)

if __name__ == "__main__":
    print('tasks path: ' + os.getcwd())