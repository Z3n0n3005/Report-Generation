import concurrent.futures
import os
import ntpath
import requests
import concurrent
from grobid_client.client import ApiClient


url = 'http://127.0.0.1:5000/summarize'
pdf_folder = 'C:\\Users\\DELL\\Prototype\\Report-Generation\\paper'

pdf_path = 'C:\\Users\\DELL\\Prototype\\Report-Generation\\paper\\a-brief-survey-of-text-mining.pdf'

def get_output_file_name(input_file, input_path, output):
    if output is not None:
        input_file_name = str(os.path.relpath(os.path.abspath(input_file), input_path))
        filename = os.path.join(
            output, os.path.splitext(input_file_name)[0] + ".grobid.tei.xml"
        )
    else:
        input_file_name = ntpath.basename(input_file)
        filename = os.path.join(
            ntpath.dirname(input_file),
            os.path.splitext(input_file_name)[0] + ".grobid.tei.xml",
        )

    return filename

def upload_file(file_path, url):
    with open(file_path, "rb") as pdf_handle:
        files = {'files': pdf_handle}
        return requests.post(url, files=files) 

def main():
    input_file_paths = []
    for (dirpath, dirnames, filenames) in os.walk(pdf_folder):
        for filename in filenames:
            if filename.endswith('.pdf'):
                input_file_paths.append(os.sep.join([dirpath, filename])) 
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        results = executor.map(
            upload_file,
            input_file_paths,
            [url] * len(input_file_paths)
        )
    return


if __name__ == "__main__":
    main()