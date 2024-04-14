from segment import Segment

class Paper:
    def __init__(self):
        self.id = -1
        self.name = ""
        self.segment_list:list[Segment] = []
    
    def set_abstract_seg(self, abstract_segment:str):
        self.abstract_segment = abstract_segment
    
    def set_name(self, name:str):
        self.name = name

    def set_id(self, id:int):
        self.id = id

    def append_to_segment_list(self, segment:Segment):
        self.segment_list.append(segment)
    
    def set_segment_list(self, segment_list:list[Segment]):
        self.segment_list = segment_list

    def __str__(self) -> str:
        result = "Abstract: " + self.abstract_segment + "\n"
        for segment in self.segment_list:
            result += "Header: " + segment.get_header() + "\n"
            result += "Content: " + segment.get_content()[0:100] + "...\n"
        return result

    def get_segment_list(self) -> list[Segment]:
        return self.segment_list
    
    def get_segment_by_index(self, index:int) -> Segment:
        # for segment in self.get_segment_list():
            
        return self.get_segment_list()[index]
    
    def get_segment_by_name(self, header_name:str) -> Segment:
        result = None
        for segment in self.get_segment_list():
            if(segment.get_header() == header_name):
                result = segment
                break
        return result
    
    def get_abstract_segment(self) -> str:
        return self.abstract_segment

    def get_name(self) -> str:
        return self.name
    
    def get_id(self) -> int:
        return self.id

    def to_json_format(self) -> dict:
        """
        Format the entire paper into json format
        """
        result = {}
        result["id"] = self.id
        result["name"] = self.name
        result["abstract_seg"] = self.abstract_segment
        result["segments"] = []
        for segment in self.segment_list:
            segment_dict = {}
            segment_dict["header"] = segment.get_header()
            segment_dict["content"] = segment.get_content()
            result["segments"].append(segment_dict)
        return result

    
    def clean(self):
        '''
        Remove segments with no header or content
        '''
        segments_to_remove = []
        for segment in self.segment_list:
            header = segment.get_header()
            if(header == ''):
                segments_to_remove.append(segment)
                continue
            
            content = segment.get_content()
            if(content == ''):
                segments_to_remove.append(content)
                continue
        
        for segment in segments_to_remove:
            self.segment_list.remove(segment)
                