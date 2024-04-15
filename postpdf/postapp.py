import concurrent.futures
import os
import ntpath
import requests
# import concurrent
from concurrent.futures import ThreadPoolExecutor, wait
from grobid_client.client import ApiClient

url_base = 'http://127.0.0.1:5000'
url_upload = '/upload'
url_summarize = '/summarize'
pdf_folder = 'C:\\Users\\DELL\\Prototype\\Report-Generation\\paper'

pdf_path = 'C:\\Users\\DELL\\Prototype\\Report-Generation\\paper\\a-brief-survey-of-text-mining.pdf'

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
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(
            upload_file,
            input_file_paths,
            [url_base + url_upload] * len(input_file_paths)
        )
        
        for result in results:
            print(result.content)
        
        # for r in result:
        #     print(r)
        # wait(timeout=5)
    response = requests.post(url=url_base + url_summarize)
    print(response.json())
    return

if __name__ == "__main__":
    main()