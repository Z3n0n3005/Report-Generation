import nltk 

def rouge_n(ref:str, test:str, n:int):
    ref_list = nltk.word_tokenize(ref)
    test_list = nltk.word_tokenize(test)

    ref_n_gram = list(nltk.ngrams(ref_list, n))
    test_n_gram = list(nltk.ngrams(test_list, n))

    match_list = []
    for ref in ref_n_gram:
        if(ref in test_n_gram): match_list.append(ref)

    # print(set(match_list))
    # print(set(ref_n_gram))

    f_measure = nltk.f_measure(set(match_list), set(ref_n_gram)) 
    if(f_measure is None): f_measure = 0

    return f_measure

def rouge_l(ref:str, test:str):
    return

def main():
    print(rouge_n("hi there", "hello there", 2))

if __name__ == "__main__":
    main()    