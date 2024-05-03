import concurrent.futures
import os
import ntpath
import requests
# import concurrent
from concurrent.futures import ThreadPoolExecutor, wait
from grobid_client.client import ApiClient

ip_local_host = '127.0.0.1'
ip_local_router = '192.168.100.28'
url_base = 'http://' + ip_local_router + ':5000'
url_upload = '/upload'
url_summarize = '/summarize'
url_connect_to_zotero = '/connectToZotero'
url_get_pdf_file_zotero = '/getPdfFileZotero'
pdf_folder = 'C:\\Users\\DELL\\Prototype\\Report-Generation\\paper'

pdf_path = 'C:\\Users\\DELL\\Prototype\\Report-Generation\\paper\\a-brief-survey-of-text-mining.pdf'

pdf_path = '/media/vy/vy/prototype/Report-Generation/docker/resources/temp/pdf_in/Deienno_et_al._-_2024_-_Accretion_and_Uneven_Depletion_of_the_Main_Asteroi.pdf'

pdf_folder = '/media/vy/vy/prototype/Report-Generation/docker/resources/temp/pdf_in'

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
    # main()

    file_header = {
        'Api-Key':'IqssCl6uXkPQqcMP6y52Enj2', 
        'Library-Id':'14142718',
        'Library-Type':'user',
        'Item-Key':'SNXV9A8F'
    }
    session = requests.Session()
    # response = session.post(
    #     url=url_base+url_connect_to_zotero,
    #     headers = session_headers
    # )
   
    # print(response.request.headers)
    response = session.post(
        url = url_base + url_get_pdf_file_zotero, 
        headers = file_header
    )
    # response.headers.update(file_header)
    print(response.request.headers)

    reponse = session.post(
        url = url_base + url_summarize
    )
    print(response.request)