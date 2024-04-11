import config
import os
from paper import Paper
import xml.etree.ElementTree as ET

SEGMENT_FOLDER = config.get_segment_path()

def parse_xml_folder():
    files = []
    print(os.getcwd() + SEGMENT_FOLDER)
    # Get all file path list
    for (dirpath, _, filenames) in os.walk(SEGMENT_FOLDER):
        for filename in filenames:
            if filename.endswith('.tei.xml'):
                files.append(os.sep.join([dirpath, filename]))
    print(files)
    # May put threadpoolexecutor here if its slow
    for file in files:
        parse_xml_file(file)

def parse_xml_file(file):
    tree = ET.parse(file)    
    root = tree.getroot()
    print(root)


if __name__ == "__main__":
    print(SEGMENT_FOLDER)
    parse_xml_folder()