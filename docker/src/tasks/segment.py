class Segment:
    def __init__(self, header:str="", content:str=""):
        self.header = header
        self.content = content
        
    def __str__(self) -> str:
        result = "-----------\n"
        result += "HEADER: " 
        result += self.header + "\n"
        result += "CONTENT: \n"
        result += self.content + "\n"
        return result

    def set_header(self, header:str):
        self.header = header
    
    def set_content(self, content:str):
        self.content = content

    def get_header(self):
        return self.header

    def get_content(self):
        return self.content

    def add_content(self, content:str):
        if(content == None):
            return 
        self.content += content

    def to_dict(self):
        return {
            'header': self.header,
            'content': self.content
        }
    
    @staticmethod
    def from_dict(data):
        return Segment(
            header = data['header'],
            content = data['content']
        )

if __name__ == "__main__":
    segment = Segment("header", "content")
    segment_dict = segment.to_dict()
    segment_obj = Segment.from_dict(segment_dict)
    print(segment_dict)
    print(segment_obj)