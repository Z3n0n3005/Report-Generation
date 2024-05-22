import sys
import json
import time
import config
# sys.path.insert(1, '/code/lib/grobid_client_python/')
from grobid_client.grobid_client import GrobidClient
import app
from flask import current_app
import concurrent.futures

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

async def parse_pdf() -> bool:
    start_time = time.time()
    with app.app.app_context():
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            try:
                client = GrobidClient(config_path=GROBID_CONFIG_PATH)
                client.process("processFulltextDocument", UPLOAD_FOLDER, output=SEGMENT_FOLDER, consolidate_citations=False, tei_coordinates=False, verbose=True)
            except:
                return False
    end_time = time.time()
    app.app.logger.info("Grobid parse pdf time: " + str(end_time - start_time))
    
    return True

if __name__ == "__main__":
    parse_pdf()