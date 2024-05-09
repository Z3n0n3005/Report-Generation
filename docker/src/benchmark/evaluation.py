from nltk import word_tokenize, ngrams, f_measure
from difflib import SequenceMatcher
from enum import Enum

class EvalMethod(Enum):
    ROUGE_1 = 'rouge_1'
    ROUGE_2 = 'rouge_2'
    ROUGE_L = 'rouge_l'

def rouge_n(test:str, ref:str, n:int) -> float:
    ref_list = word_tokenize(ref)
    test_list = word_tokenize(test)

    ref_n_gram = list(ngrams(ref_list, n))
    test_n_gram = list(ngrams(test_list, n))

    match_list = []
    for ref in test_n_gram:
        if(ref in ref_n_gram): match_list.append(ref)

    # print(set(match_list))
    # print(set(ref_n_gram))

    result = f_measure(set(match_list), set(test_n_gram)) 
    if(result is None): result = 0

    return result

def rouge_1(test:str, ref:str) -> float:
    return rouge_n(test, ref, 1)

def rouge_2(test:str, ref:str) -> float:
    return rouge_n(test, ref, 2)

def rouge_l(test:str, ref:str) -> float:
    match_info = SequenceMatcher(None, test, ref).find_longest_match()
    longest_match = test[match_info.a : match_info.a + match_info.size]
    
    longest_match_uni_gram = list(ngrams(longest_match, 1))
    ref_uni_gram = list(ngrams(ref, 1))

    # print(set(longest_match_uni_gram))
    # print(set(ref_uni_gram))

    result = f_measure(set(longest_match_uni_gram), set(ref_uni_gram))
    return result

eval_method_dict = {
    EvalMethod.ROUGE_1.value : rouge_1,
    EvalMethod.ROUGE_2.value : rouge_2,
    EvalMethod.ROUGE_L.value : rouge_1    
}

def main():
    test = 'A fast brown fox leaps over a sleeping dog.'
    ref = 'The quick brown fox jumps over the lazy dog.'
    print(rouge_n(test, ref, 1))
    print(rouge_n(test, ref, 2))
    print(rouge_l(test, ref))

if __name__ == "__main__":
    main()    