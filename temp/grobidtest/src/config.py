import json

class Config:
    def __init__(self, path:str):
        config_json = open(path).read()
        self.config = json.loads(config_json)

    def get_resource_path(self) -> str:
        return self.config_json["resource_folder"]
        
    def get_upload_path(self) -> str:
        upload = self.config_json["upload_folder"]
        return self.get_resource_path() + upload
    
    def get_segment_path(self) -> str:
        segment = self.config_json["segment_folder"]
        return self.get_resource_path() + segment
    
    def get_summary_path(self) -> str:
        summary = self.config_json["summary_folder"]
        return self.get_resource_path() + summary