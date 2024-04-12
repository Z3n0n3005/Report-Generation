import config
import os
from paper import Paper
from segment import Segment
import xml.etree.ElementTree as ET

SEGMENT_FOLDER = config.get_segment_path()

def parse_xml_folder():
    files = []
    papers:list[Paper] =[]
    # Get all file path list
    for (dirpath, _, filenames) in os.walk(SEGMENT_FOLDER):
        for filename in filenames:
            if filename.endswith('.tei.xml'):
                files.append(os.sep.join([dirpath, filename]))
    # May put threadpoolexecutor here if its slow
    for file in files:
        # Create new paper
        paper = get_xml_parsing_result(file)
        # Append paper to list
        papers.append(paper)

def get_xml_parsing_result(file) -> Paper:
    paper = Paper()
    paper.set_abstract_seg(get_abstract(file))
    
    paper.set_segment_list(get_segment_list(file))
    
    
    
    return paper

def get_abstract(file) -> str:
    result = ""
    namespace = get_namespace()
    tree = ET.parse(file)
    root = tree.getroot()
    for abstract in root.findall(".//tei:abstract", namespace):
        for div in abstract.findall("tei:div", namespace):
            p = div.findall("tei:p", namespace)
            result = p
    return result
    
def get_segment_list(file) -> list[Segment]:
    segments = []
    namespace = get_namespace()
    tree = ET.parse(file)
    root = tree.getroot()
    for body in root.findall(".//tei:body", namespace):
        for div in body.findall("tei:div", namespace):
            segment = Segment()
            header = div.find("tei:head", namespace)
            header_number = header.get("n")
            if(header_number == None):
                header_number = ""

            print("header: " + header.text + " " + header_number)
            segment.set_header(header.text)

            content = ""
            for p in div.findall("tei:p", namespace):
                content.join([p.text, "\n"])
            segment.set_content(content)
        print(segment)
        segments.append(segment)
    return segments

def iter_and_print(elem):
    for e in elem.iter():
        print(e)
    
def get_namespace() -> dict:
    return {'tei':'http://www.tei-c.org/ns/1.0'}

if __name__ == "__main__":
    parse_xml_folder()