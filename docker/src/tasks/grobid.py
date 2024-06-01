import time
from . import config
from grobid_client.grobid_client import GrobidClient
from celery_app import app

# Linux paths
# UPLOAD_FOLDER = '/code/resources/pdf_in'
# SEGMENT_FOLDER = '/code/resources/pdf_segment'
# GROBID_config_PATH = '/code/config.json'
# Window paths
# UPLOAD_FOLDER = 'resources\\pdf_in'
# SEGMENT_FOLDER = 'resources\\pdf_segment'
# GROBID_config_PATH = 'config.json'

UPLOAD_FOLDER = config.get_upload_path()
SEGMENT_FOLDER = config.get_segment_path()
GROBID_CONFIG_PATH = config.get_config_path()

@app.task()
async def parse_pdf() -> bool:
    start_time = time.time()
    try:
        client = GrobidClient(config_path=GROBID_CONFIG_PATH)
        client.process("processFulltextDocument", UPLOAD_FOLDER, output=SEGMENT_FOLDER, consolidate_citations=False, tei_coordinates=False, verbose=True)
    except:
        return False
    end_time = time.time()
    print("Grobid Parse time: " + str(end_time - start_time))
    return True

if __name__ == "__main__":
    parse_pdf()