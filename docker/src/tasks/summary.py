import os
import tasks
from tasks.paper import Paper, PaperDecoder, PaperEncoder
from log.log_util import log
from enum import Enum
from tasks.segment import Segment
import json
import time
import app
import tasks.summary_technique.textrank as textrank
import tasks.summary_technique.lsa as lsa
import tasks.summary_technique.model as model
import tasks.config as config
from celery_app import app

SUMMARY_FOLDER = config.get_summary_path()
SEGMENT_JSON_FOLDER = config.get_segment_json_path()
PREPROCESS_SENT_NUM = 10

class PreProcessAlgo(Enum):
    NONE = "none"
    TEXTRANK = "textrank"
    LSA = "lsa"

class SumAlgo(Enum):
    TEXTRANK = "textrank"
    LSA = "lsa"
    FALCON = "falcon_text_summarizer"
    GEMMA_2B = "gemma_2b"
    STABLE_LM = "stable_lm_chat"
    BART_LARGE_CNN = "bart_large_cnn"
    ZEPHYR = "zephyr"

algo = {
    SumAlgo.TEXTRANK.value : textrank.summarize_text,
    SumAlgo.LSA.value : lsa.summarize_text, 
    SumAlgo.FALCON.value : model.falcon_ai_text_summarizer,
    SumAlgo.STABLE_LM.value : model.stable_lm_chat_1_6b,  
    SumAlgo.BART_LARGE_CNN.value : model.bart_large_cnn,
    SumAlgo.ZEPHYR.value : model.zephyr,
    SumAlgo.GEMMA_2B.value : model.gemma_1_1_2b_it
}

algo_using_lm = [
    SumAlgo.FALCON,
    SumAlgo.STABLE_LM,
    SumAlgo.BART_LARGE_CNN,
    SumAlgo.ZEPHYR,
    SumAlgo.GEMMA_2B
]

preload = {
    SumAlgo.FALCON.value : model.preload_falcon_ai_text_summarizer,
    SumAlgo.STABLE_LM.value : model.preload_stable_lm_chat_1_6b,
    SumAlgo.BART_LARGE_CNN.value : model.preload_bart_large_cnn,
    SumAlgo.ZEPHYR.value : model.preload_zephyr,
    SumAlgo.GEMMA_2B.value : model.gemma_1_1_2b_it    
}

preprocessing = {
    PreProcessAlgo.NONE.value : lambda text : text,
    PreProcessAlgo.TEXTRANK.value : lambda content : textrank.preprocess_input(content, 5),
    PreProcessAlgo.LSA.value : lambda content : lsa.preprocess_input(content, 10)
}

@app.task
def summarize_folder(preprocess_algo:str, sum_algo:str) -> list[Paper]:
    start_time = time.time()

    papers = get_paper_list_from_folder()
    s_papers = []
    # Preload the model if it use LM
    if(sum_algo in algo_using_lm):
        preload[sum_algo]()
        
    for paper in papers:    
        s_paper_result = summarize_content.delay(paper, preprocess_algo, sum_algo)
        s_paper = s_paper_result.get()
        s_papers.append(s_paper)

    end_time = time.time()
    print("Summarize folder: " + str(end_time - start_time))
    return s_papers

def get_paper_list_from_folder() -> list[Paper]:
    papers = []
    for filename in os.listdir(SEGMENT_JSON_FOLDER):
        file_path = os.path.join(SEGMENT_JSON_FOLDER, filename)
        if os.path.isfile(file_path) and filename.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    paper = json.load(file, cls=PaperDecoder)
                    papers.append(paper)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {file_path}: {e}")
    return papers

@app.task
def summarize_content(paper:Paper, preprocess_algo:str, sum_algo:str) -> list[dict]:
    id = paper.get_id()
    name = paper.get_name()
    abstract_seg = paper.get_abstract_segment()
    segment_list = paper.get_segment_list()
    s_paper = Paper()
    s_paper.set_id(id)
    s_paper.set_name(name)

    s_paper.set_abstract_seg(abstract_seg)
    for segment in segment_list:
        s_segment_result = summarize_segment.delay(segment, preprocess_algo, sum_algo)
        s_segment = Segment.from_dict(s_segment_result.get())
        s_paper.append_to_segment_list(s_segment)
    
    save_to_folder([s_paper])
    return s_paper.to_dict()

@app.task
def summarize_segment(segment:Segment, preprocess_algo:str, sum_algo:str) -> Segment:
    s_segment = Segment()
    header = segment.get_header()
    content = segment.get_content()
    content_pre_process = ""
    s_content = ""

    # Auto adjust the input if exceed token count
    is_no_content = False
    is_not_exceed_token = True
    sent_num = 5
    while(is_not_exceed_token and sent_num >= 1 and not is_no_content):
        log("[summary]", is_not_exceed_token, sent_num, is_no_content)
        if(len(content) != 0):
            content_pre_process = preprocessing[preprocess_algo](content)
        else:
            is_no_content = True

        if(len(content_pre_process) != 0):
            try:
                s_content_result = algo[sum_algo].delay(content_pre_process)
                s_content = s_content_result.get()
                is_not_exceed_token = False
            except:
                is_not_exceed_token = True
                sent_num -= 1
        else:
            is_no_content = True

    log("[model] summary result: " + s_content)
    s_segment.set_header(header)
    s_segment.set_content(s_content)
    return s_segment
            
def save_to_folder(papers:list[Paper]):
    for paper in papers:
        path = os.path.join(SUMMARY_FOLDER, paper.get_name() + ".json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(paper.to_json_format()))
    return

def get_stop_word_list() -> str:
    result = []
    stop_word_path = os.path.join(tasks.get_util_path(), "stopwords.txt")
    with open(stop_word_path, 'r', encoding="utf-8") as f:
        result = f.read().split("\n")
    return result

if __name__ == "__main__":
    print(SumAlgo.LSA.value)