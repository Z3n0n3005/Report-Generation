from tasks.paper import Paper, PaperDecoder 
import json
import os

def get_paper_from_folder(folder_path:str, file_name:str, extension:str) -> Paper:
    path = os.path.join(folder_path, file_name + "." + extension)
    with open(path, "r", encoding="utf-8") as file:
        try:
            paper = json.load(file, cls=PaperDecoder)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file {path}: {e}")
    return paper
