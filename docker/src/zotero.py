from pyzotero import zotero
from flask import current_app
import concurrent.futures
import app
import config
import time

class Zotero:
    def __init__(self, library_id, library_type, api_key):
        self.zotero = zotero.Zotero(
            library_type=library_type,
            library_id = library_id,
            api_key=api_key,
        )
    
    def get_item(self, item_key:str) -> str:
        return self.zotero.item(item_key)
        
    async def get_pdf_file(self, item_key:str, path:str=None) -> bool:
        with app.app.app_context():
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                try:
                    
                    start = time.time()
                    filename = item_key + "_" + self.zotero.item(item_key)["data"]["filename"]
                    self.zotero.dump(item_key, filename, path)
                    end = time.time()
                    app.app.logger.info(end - start)
                except:
                    return False
                return True
    
    def get_all_pdf_file(self) -> bool:
        pdf_key_list = []
        for item in self.zotero.items():
            has_links_tag = 'links' in item
            if(not has_links_tag): continue

            has_enclosure_tag = 'enclosure' in item['links']
            if(not has_enclosure_tag): continue

            is_pdf = item['links']['enclosure']['type'] == 'application/pdf'
            if(not is_pdf): continue
            
            pdf_key_list.append(item['key'])

        current_app.logger.info(pdf_key_list)
        for key in pdf_key_list:
            result = self.get_pdf_file(key, config.get_upload_path())
            if(result):
                print(key, ": Succeed")
            else:
                print(key, ": Failed")
        return True

    def is_zotero_init(self) -> bool:
        if(self.zotero.api_key == None):
            return True
        return False

def main():
    zot = Zotero('14142718', 'user', 'IqssCl6uXkPQqcMP6y52Enj2')
    # zot.get_pdf_file('SNXV9A8F', None, config.get_upload_path())
    zot.get_all_pdf_file()
    return
    

if __name__ == "__main__":
    main()