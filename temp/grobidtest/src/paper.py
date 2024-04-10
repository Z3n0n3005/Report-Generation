from segment import Segment

class Paper:
    def __init__(self):
        self.segment_list:list[Segment] = []
    
    def append_section_list(self, segment:Segment):
        self.segment_list.append(segment)
    
    def set_abstract_seg(self, abstract_segment:str):
        self.abstract_segment = abstract_segment
    
    def __str__(self) -> str:
        result = "Abstract: " + self.abstract_segment + "\n"
        for segment in self.segment_list:
            result += "Header: " + segment.get_header() + "\n"
            result += "Content: " + segment.get_content() + "\n"
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