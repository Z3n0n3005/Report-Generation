import sys
import json
import time
import config
sys.path.insert(1, '/code/lib/grobid_client_python/')
from grobid_client.grobid_client import GrobidClient

# Linux paths
# UPLOAD_FOLDER = '/code/resources/pdf_in'
# SEGMENT_FOLDER = '/code/resources/pdf_segment'
# GROBID_CONFIG_PATH = '/code/config.json'
# Window paths
# UPLOAD_FOLDER = 'resources\\pdf_in'
# SEGMENT_FOLDER = 'resources\\pdf_segment'
# GROBID_CONFIG_PATH = 'config.json'

UPLOAD_FOLDER = config.get_upload_path()
SEGMENT_FOLDER = config.get_segment_path()
GROBID_CONFIG_PATH = config.get_config_path()

def _read_json(file_path):
    with open(file_path, "r") as file:
        # Read the entire file content
        data = json.load(file)
        print(data)

def parse_pdf():
    print('hello')

    client = GrobidClient(config_path=GROBID_CONFIG_PATH)
    client.process("processFulltextDocument", UPLOAD_FOLDER, output=SEGMENT_FOLDER, consolidate_citations=False, tei_coordinates=False, verbose=True)

    # client = GrobidClient(config_path="C:\\Users\\DELL\\Prototype\\docker-compose-practice\\grobidtest\\config.json")
    # client.process("processFulltextDocument", "C:\\Users\\DELL\\Prototype\\docker-compose-practice\\grobidtest\\resources\\test_in", output="C:\\Users\\DELL\\Prototype\\docker-compose-practice\\grobidtest\\resources\\test_out", consolidate_citations=True, tei_coordinates=True, verbose=True, n=20)
    
    return 

if __name__ == "__main__":
    parse_pdf()