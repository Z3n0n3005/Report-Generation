from summa.summarizer import summarize
import summary

def summarize_text(text:str) -> str:
    return summarize(
        text = text, 
        words = _get_max_length_sentence(text) + 5,
        additional_stopwords= summary.get_stop_word_list()
    )

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