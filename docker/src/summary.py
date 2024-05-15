import os
import config
from paper import Paper
from enum import Enum
from segment import Segment
import json
import time
import app
import summary_technique.textrank as textrank
import summary_technique.lsa as lsa
import summary_technique.model as model

SUMMARY_FOLDER = config.get_summary_path()

class SumAlgo(Enum):
    TEXTRANK = "textrank"
    LSA = "lsa"
    FALCON_TEXT_SUMMARIZER = "falcon_text_summarizer"
    GEMMA_2B = "gemma_2b"
    STABLE_LM_CHAT = "stable_lm_chat"
    BART_LARGE_CNN = "bart_large_cnn"
    ZEPHYR = "zephyr"

algo = {
    SumAlgo.TEXTRANK : textrank.summarize_text,
    SumAlgo.LSA : lsa.summarize_text, 
    SumAlgo.FALCON_TEXT_SUMMARIZER : model.falcon_ai_text_summarizer,
    SumAlgo.STABLE_LM_CHAT : model.stable_lm_chat_1_6b,  
    SumAlgo.BART_LARGE_CNN : model.bart_large_cnn,
    SumAlgo.ZEPHYR : model.zephyr 
}

def summarize_folder(papers:list[Paper], sum_algo:str) -> list[Paper]:
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
            s_content = algo[sum_algo](content)
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

if __name__ == "__main__":
    print(SumAlgo.LSA.value)