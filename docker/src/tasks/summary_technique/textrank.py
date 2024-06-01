from summa.summarizer import summarize
import tasks.summary as summary
from celery_app import app

SENT_NUM = 1
PREPROCESS_SENT_NUM = 5 

def preprocess_input(text:str, sent_num:str=PREPROCESS_SENT_NUM) -> str:
    result = summarize(
        text = text, 
        words = sent_num * _get_max_length_sentence(text),
        additional_stopwords = summary.get_stop_word_list()
    )
    print("[textrank preprocess]", result)
    return result

@app.task()
def summarize_text(text:str, sent_num:int=SENT_NUM) -> str:
    return summarize(
        text = text, 
        words = sent_num * (_get_max_length_sentence(text) + 5), additional_stopwords= summary.get_stop_word_list())

def _get_max_length_sentence(text:str) -> int:
    sentences = text.split(". ")  # Split by ". " considering spaces after period
    if not sentences:
        return None
    return _get_word_count(max(sentences, key=len))

def _get_word_count(text:str) -> int:
    words = text.split(" ")
    if not words:
        return None
    return len(words)


if __name__ == "__main__":
    print("textrank")