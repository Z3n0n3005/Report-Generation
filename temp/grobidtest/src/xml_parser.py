import config
import os
from paper import Paper
from segment import Segment
import xml.etree.ElementTree as ET
import re

SEGMENT_FOLDER = config.get_segment_path()

def parse_xml_folder() -> list[Paper]:
    files = []
    papers:list[Paper] =[]
    # Get all file path list
    for (dirpath, _, filenames) in os.walk(SEGMENT_FOLDER):
        for filename in filenames:
            if filename.endswith('.tei.xml'):
                files.append(os.sep.join([dirpath, filename]))
    # May put threadpoolexecutor here if its slow
    for file in files:
        print(file)
        # Create new paper
        paper = get_xml_parsing_result(file)
        # Append paper to list
        papers.append(paper)
    return papers

def get_xml_parsing_result(file) -> Paper:
    paper = Paper()
    paper.set_abstract_seg(get_abstract(file))
    paper.set_segment_list(get_segment_list(file))
    
    print(paper)
    
    return paper

def get_abstract(file) -> str:
    result = ""
    namespace = get_namespace()
    tree = ET.parse(file)
    root = tree.getroot()
    for abstract in root.findall(".//tei:abstract", namespace):
        for div in abstract.findall("tei:div", namespace):
            p = div.find("tei:p", namespace)
            result = p.text
    return result
    
def get_segment_list(file) -> list[Segment]:
    segments = []
    namespace = get_namespace()
    tree = ET.parse(file)
    root = tree.getroot()
    for body in root.findall(".//tei:body", namespace):
        segment = Segment()
        prev_header_number = -1
        for div in body.findall("tei:div", namespace):
            header = div.find("tei:head", namespace)
            header_number = header.get("n")

            if(header_number == None):
                header_number = prev_header_number[0] + ".0"

            main_header_number = header_number[0]
            
            # print(main_header_number, prev_header_number)
            
            # First time pass:w
        
            if(prev_header_number == -1):
                prev_header_number = main_header_number
                segment.set_header(header.text)

            # Current header is differnt than old header
            if(main_header_number != prev_header_number):
                prev_header_number = main_header_number
                segments.append(segment)
                # print(segment)
                segment = Segment()
                segment.set_header(header.text)

            # Add content to current segment
            for p in div.findall("tei:p", namespace):
                segment.add_content(p.text)
        
        # Add the last segment to list
        segments.append(segment)
    return segments

def iter_and_print(elem):
    for e in elem.iter():
        print(e)
    
def get_namespace() -> dict:
    return {'tei':'http://www.tei-c.org/ns/1.0'}

if __name__ == "__main__":
    print(SEGMENT_FOLDER)
    parse_xml_folder()