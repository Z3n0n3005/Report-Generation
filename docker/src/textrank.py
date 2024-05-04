from summa.summarizer import summarize
import argparse
import os
import config
from paper import Paper
from segment import Segment
import json
import time
import app

SUMMARY_FOLDER = config.get_summary_path()

def summarize_folder(papers:list[Paper]) -> list[Paper]:
    start_time = time.time()
    s_papers = []
    for paper in papers:
        id = paper.get_id()
        name = paper.get_name()
        abstract_seg = paper.get_abstract_segment()
        segment_list = paper.get_segment_list()
        s_paper = Paper()
        s_paper.set_id(id)
        s_paper.set_name(name)
        
        s_paper.set_abstract_seg(abstract_seg)
        for segment in segment_list:
            s_segment = Segment()
            header = segment.get_header()
            content = segment.get_content()
            s_content = summarize_text(content)
            s_segment.set_header(header)
            s_segment.set_content(s_content)
            s_paper.append_to_segment_list(s_segment)
        s_papers.append(s_paper)
    end_time = time.time()
    app.app.logger.info("Summarize folder: " + str(end_time - start_time))
    return s_papers

def save_to_folder(papers:list[Paper]):
    for paper in papers:
        path = os.path.join(SUMMARY_FOLDER, paper.get_name() + ".json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(paper.to_json_format()))
    return

def get_stop_word_list() -> str:
    result = []
    stop_word_path = os.path.join(config.get_util_path(), "stopwords.txt")
    with open(stop_word_path, 'r', encoding="utf-8") as f:
        result = f.read().split("\n")
    return result

def summarize_text(text:str) -> str:
    return summarize(
        text = text, 
        words = get_max_length_sentence(text) + 5,
        additional_stopwords=get_stop_word_list()
    )
    # return summarize(
    #     text=text, 
    #     ratio=0.2,
    #     additional_stopwords=get_stop_word_list(), 
    #     words=50
    # )

def get_max_length_sentence(text:str) -> int:
    sentences = text.split(". ")  # Split by ". " considering spaces after period
    if not sentences:
        return None
    return get_word_count(max(sentences, key=len))

def get_word_count(text:str) -> int:
    
    words = text.split(" ")
    if not words:
        return None
    return len(words)

if __name__ == "__main__":
    print("textrank")