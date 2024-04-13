import config
import os
from paper import Paper
from segment import Segment
import xml.etree.ElementTree as ET
import re

SEGMENT_FOLDER = config.get_segment_path()
SEGMENT_FILE_PATH = ".grobid.tei.xml"

def parse_xml_folder() -> list[Paper]:
    files = []
    papers_name:list[str] = []
    papers:list[Paper] = []
    # Get all file path list
    for (dirpath, _, filenames) in os.walk(SEGMENT_FOLDER):
        for filename in filenames:
            if filename.endswith('.tei.xml'):
                files.append(os.sep.join([dirpath, filename]))
                papers_name.append(filename)
                
    # May put threadpoolexecutor here if its slow
    for i in range(len(files)):
        file = files[i]
        paper_name = papers_name[i] 

        # Create new paper
        paper = get_xml_parsing_result(file)
        paper.set_name(paper_name.removesuffix(SEGMENT_FILE_PATH))
        print(paper.get_name())
        paper.clean()

        # Append paper to list
        papers.append(paper)

    return papers

def get_xml_parsing_result(file) -> Paper:
    paper = Paper()
    paper.set_abstract_seg(get_abstract(file))
    paper.set_segment_list(get_segment_list(file))
    # print(paper.to_json_format())
    
    return paper

def get_abstract(file) -> str:
    result = ""
    namespace = get_namespace()
    tree = ET.parse(file)
    root = tree.getroot()
    # Get all <abstract> 
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
    
    # Get all <body>
    for body in root.findall(".//tei:body", namespace):
        segment = Segment()
        prev_header_number = "-1"

        # Get all <div>
        for div in body.findall("tei:div", namespace):
            # Get <head>
            header = div.find("tei:head", namespace)
            # Get value of <head n="...">
            header_number = header.get("n")

            if(header_number == None):
                # In case no header number is found in the entire file
                key = 0
                if(prev_header_number == -1):
                    key = 1

                # print(prev_header_number[key])
                header_number = prev_header_number[key] + ".0"

            main_header_number = header_number[0]
            
            # print(main_header_number, prev_header_number)
            
            # First time pass
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