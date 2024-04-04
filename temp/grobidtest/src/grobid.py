import sys
import json
import time
sys.path.insert(1, '/code/lib/grobid_client_python/')
from grobid_client.grobid_client import GrobidClient

def _read_json(file_path):
    with open(file_path, "r") as file:
        # Read the entire file content
        data = json.load(file)
        print(data)

def parse_pdf():
    print('hello')

    client = GrobidClient(config_path="/code/config.json")
    client.process("processFulltextDocument", "/code/resources/test_in", output="/code/resources/test_out/", consolidate_citations=True, tei_coordinates=True, verbose=True)
    
    # client = GrobidClient(config_path="C:\\Users\\DELL\\Prototype\\docker-compose-practice\\grobidtest\\config.json")
    # client.process("processFulltextDocument", "C:\\Users\\DELL\\Prototype\\docker-compose-practice\\grobidtest\\resources\\test_in", output="C:\\Users\\DELL\\Prototype\\docker-compose-practice\\grobidtest\\resources\\test_out", consolidate_citations=True, tei_coordinates=True, verbose=True, n=20)
    
    return 