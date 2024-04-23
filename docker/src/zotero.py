from pyzotero import zotero

class Zotero:
    def __init__(self, library_id, library_type, api_key):
        self.zotero = zotero.Zotero(
            library_type=library_type,
            library_id = library_id,
            api_key=api_key,
        )
    
    def get_item(self, item_key:str) -> str:
        return self.zotero.item(item_key)
        
    def get_pdf_file(self, item_key:str, file_name:str=None, path:str=None) -> str:
        return self.zotero.dump(item_key, file_name, path)
    
    # def __init__(self):
    #     self.__init__(self, None, None, None)

    def init_zotero(library_id, library_type, api_key):
        return 

def main():
    print(zot.get_pdf_file('SNXV9A8F'))
    return

if __name__ == "__main__":
    main()