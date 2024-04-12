class Segment:
    def __init__(self, header:str, content:str):
        self.header = header
        self.content = content
        
    def __init__(self):
        self.header = ""
        self.content = ""

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
