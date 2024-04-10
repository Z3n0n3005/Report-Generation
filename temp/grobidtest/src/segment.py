class Segment:
    def __init__(self, header:str, content:str):
        self.header = header
        self.content = content
        
    def get_header(self):
        return self.header

    def get_content(self):
        return self.content
