import config
import os
from paper import Paper
from segment import Segment
from log.log_util import log
import app
import xml.etree.ElementTree as ET
import re
import summary
import time
import asyncio

SEGMENT_FOLDER = config.get_segment_path()
SEGMENT_FILE_PATH = ".grobid.tei.xml"
IS_TRUNCATING_FILE_NAME = False

def parse_xml_folder(filename:str=None) -> list[Paper]:
    start_time = time.time()
    files = []
    papers_name:list[str] = []
    papers:list[Paper] = []
    # Get all file path list
    for (dirpath, _, filenames) in os.walk(SEGMENT_FOLDER):
        for f in filenames:
            is_end_w_tei = f.endswith('.tei.xml')
            is_file_name_provided = (
                    filename!=None 
                    and f[0:-15] == filename[0:-4]
                )
            # app.app.logger.info(filename[0:-4] + " " + f[0:-15] + " " + str(is_file_name_provided) )
            is_no_file_name = (filename == None)

            if (
                is_end_w_tei
                and is_file_name_provided
                or is_no_file_name
            ):
                files.append(os.sep.join([dirpath, f]))
                papers_name.append(f)
                
    # May put threadpoolexecutor here if its slow
    for i in range(len(files)):
        file = files[i]
        paper_name = papers_name[i] 

        # Create new paper
        paper = get_xml_parsing_result(file)
        if(IS_TRUNCATING_FILE_NAME):
            paper.set_name(paper_name.removesuffix(SEGMENT_FILE_PATH)[9:])
            paper.set_id(paper_name[0:8])
            print(paper.get_id())
        else:
            paper.set_name(paper_name)
            paper.set_id(abs(hash(paper_name)))
            print(paper.get_id())
        paper.clean()

        # Append paper to list
        papers.append(paper)
    end_time = time.time()
    app.app.logger.info("XMl Parser folder time: " + str(end_time - start_time))
    app.app.logger.info(str(papers))
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
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        # Get all <abstract> 
        for abstract in root.findall(".//tei:abstract", namespace):
            for div in abstract.findall("tei:div", namespace):
                p = div.find("tei:p", namespace)
                result = p.text
    except:
        result = ""
    return result
    
def get_segment_list(file) -> list[Segment]:
    segments = []
    namespace = get_namespace()
    try: 
        tree = ET.parse(file)
        root = tree.getroot()
    
        # Get all <body>
        for body in root.findall(".//tei:body", namespace):
            segments = parse_body(body)
    except:
        segments = [] 
        
    return segments

def parse_body(body) -> list[Segment]:
    segments = []
    namespace = get_namespace()
    segment = Segment()
    prev_header_number = "-1"
    is_no_header_num = True

    # Get all <div>
    
    # Check if there is no number in any header
    for div in body.findall("tei:div", namespace):
        header = div.find("tei:head", namespace)
        if(header == None):
            continue
        
        header_number = header.get("n")
        if(header_number != None):
            is_no_header_num = False
            break

    for div in body.findall("tei:div", namespace):
        # Get <head>
        # app.flask_log(set(div.iter()))
        header = div.find("tei:head", namespace)
        # app.flask_log(set(header.iter()))
        # Get value of <head n="...">
        if(header == None):
            continue
        # print(header.text)
        header_number = header.get("n")

        if(header_number == None):
            key = 0
            if(prev_header_number == "-1"):
                key = 1

            # print(prev_header_number[key])
            header_number = prev_header_number[key] + ".0"
            
            # In case no header number is found in the entire file
            if(is_no_header_num):
                header_number = str(int(prev_header_number) + 1)
            

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
            # print(p.remove(p.find("tei:ref", namespace)))
            # iter_and_print(p)
            segment.add_content(p.text)
            for child in p:
                if child.tail:
                    segment.add_content(child.tail)
    # Add the last segment to list
    segments.append(segment)
    return segments

def iter_and_print(elem):
    remove_ref(elem)
    for e in elem.iter():
        print(e.text)
    
def get_namespace() -> dict:
    return {'tei':'http://www.tei-c.org/ns/1.0'}

def remove_ref(elem):
    """
    Remove reference tag from a specific element (Not currently in use)
    """
    remove_list = []
    for e in elem.iter():
        # print(e.tag != "{http://www.tei-c.org/ns/1.0}ref")
        if e.tag != "{http://www.tei-c.org/ns/1.0}ref":
            continue
        if True:
            remove_list.append(e)
            
    for e in remove_list:
        elem.remove(e)
            
async def main():
    start = time.time()
    papers = parse_xml_folder()

    preprocess_algo = summary.PreProcessAlgo.LSA.value
    summary_algo = summary.SumAlgo.STABLE_LM.value

    tasks = [
        summary.summarize_folder(
            papers,
            preprocess_algo,
            summary_algo
        )
    ]
    s_papers = await asyncio.gather(*tasks)
    # summary._save_to_folder_sync(papers) 

    end = time.time()
    log("[", preprocess_algo, " - ", summary_algo, "] Total time:", str(end - start))

if __name__ == "__main__":
    asyncio.run(main())