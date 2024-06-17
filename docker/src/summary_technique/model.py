from transformers import AutoTokenizer, TFAutoModel, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from log.log_util import log
import time
import torch
# from summary import SumAlgo
from nltk import word_tokenize
import asyncio
import app

test_paragraph = "After we follow accretion in the MAB during the first 5 Myr of the solar system's history, it is necessary to account for the various processes that happened during subsequent 4.5 Gyr evolution after gas disk dispersal. Specifically, the giant planet instability has been found to heavily deplete the MAB In this work, we consider the MAB region to be delimited as follows (e.g., We then use this MAB definition to select objects from the Minor Planet Center (MPC) databaseFigure For our depletion analysis, we further divide the MAB definition above into 5 sub-regions: Extended inner Main Belt (EiMB; a < 2.1 au), Inner Main Belt (IMB; 2.1 au < a < 2.5 au), Center Main Belt (CMB; 2.5 au < a < 2.82 au), Outer Main Belt (OMB; 2.82 au < a < 3.25 au), and Extended outer Main Belt (EoMB; a > 3.25 au). The row labeled D18 D f ac in Table . D f ac effectively reports the survival fraction of objects from the simulation. Yet, we prefer to refer to them as a depletion factor as those are the numbers we directly multiply the evolved population in order to account for their depletion. Dper is for the percentage of depletion Dper \u2248 100 \u00d7 (1 -D f ac ). Labels all and AM D JS P S /P J are for different cuts in the data by \u2022 C19 all refers to results taken from \u2022 C19 AM DJS P S /P J is also for results from The work by Our analyses clearly demonstrate that MAB depletion during the giant planet instability is not uniform. The fact that different MAB sub-regions have different depletion factors was first pointed out by"
test_paragraph_1 = """
18   Likewise, instead of assuming that p i ∈ [0, 1] captures the productivity of individual i, 
we could assume that it captures the probability to succeed in life that individual i has.      
Therefore, let f i : A×[0, 1]×R + → R be such that f i (a i , p i , t i ) = t * i for each i ∈ N.
As in the models of where g : R + → R is strictly increasing.Suppose first that is represented by a PHEF satisfying andThus,Conversely, assume now that preferences satisfy all the axioms in COMMON as well as TIFHP.
Then, by Theorem 10, for each pair d, d ′ ∈ D,where g : R + → R is strictly increasing.
As g is continuous and strictly increasing, it follows from Theorem 1 in Suppose first that is represented by a PHEF satisfying Then, by Theorem 10, for each pair d, d ′ ∈ D,where = ϕ(a, p,= ϕ(a, p,In particular, ϕ(a, p, t → R be such that 
w(a, p) = ŵ(a,p) ŵ(a * ,1) , for each (a, p) ∈ A × [0, 1].
Then, we may write: ϕ(a, p, t i ) = w(a, p)t i , where 0 ≤ w(a, p) ≤ w(a * , p) ≤ w(a * , 1) = 1, and 0 ≤ w(a, p) ≤ w(a, 1) ≤ w(a * , 1) = 1 for each (a, p) ∈ A × [0, 1], as desired.Suppose first that is represented by a PHEF satisfying Then, for each c > 0,Conversely, assume now that preferences satisfy all the axioms in the statement of Theorem where g : R + → R is strictly increasing.
Then, it follows that 1 = q(a * ) ≥ q(a) ≥ 0, for each a ∈ A.And we may write:where 0 ≤ q(a) ≤ q(a * ) = 1, for each a ∈ A, as desired.Suppose first that is represented by a PHEF satisfying Then, for each c > 0,Thus, as v( and each c > 0 such that p i + c, p j + c ∈ [0, 1].
In particular, Suppose first that is represented by a PHEF satisfying Then, for each c > 0 such 
that p i + c, p j + c ≤ 1, E[(a, p i + c, t), (a, p j , t), d N \{i,j} ] = q(a)(p i + c)t + q(a)p j t + k∈N \{i,j} q(a k )p k t k , and E[(a, p 
i , t), (a, p j + c, t), d N \{i,j} ] = q(a)p i 
t + q(a)p j (t + c) + k∈N \{i,j} q(a k )p k t k 
.Thus, [(a, p i + c, t), (a, p j , t), d N \{i,j} ] ∼ [(a, p i , t), (a, p j + c, t), d N \{i,j} ].Conversely, assume now that preferences satisfy all the axioms in the statement of Theorem 5.Thus, for each pair d, d ′ ∈ D, and, therefore, 
is indeed represented by an evaluation function 
satisfying (5), as desired.Suppose first that is represented by a PHEF satisfying Conversely, assume now that preferences satisfy all the axioms in the statement of Theorem for each a ∈ A, it 
follows that is represented by an evaluation function satisfying Case 3.
Thus, for each pair d, d ′ ∈ D,where q, r : A → 
[0, 1] are such that 1 = q(a * ) ≥ q(a) ≥ 0, and 1 = r(a * ) ≥ r(a) ≥ 0 and δ ∈ (0, 1).
Consequently, is indeed represented by an evaluation function satisfying Suppose first that is represented by a PHEF satisfying where q, r : A → [0, 1] are such that 1 = q(a * ) ≥ q(a) ≥ 0, and 1 = r(a * ) ≥ r(a) ≥ 0 andBy PICT, [(a i , p i + c, t), (a j , p j , t), d N \{i,j} ] ∼ [(a i 
, p i , t), (a j , p j + c, t), d N \{i,j} ],for each d ∈ D, and i, j ∈ N with t i = t j = t."""

access_token = "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"
tokenizer = None
model = None
summarizer = None

# def preload_model(sumAlgo:SumAlgo):
#     return

def prompt_constructor(content:str) -> str:
    result = 'Summarize the following segment into 1 sentence: ' + content
    return result

def get_max_length(content:str) -> int:
    tokens = word_tokenize(content)
    return len(tokens)

async def preload_zephyr():
    start = time.time()

    global tokenizer
    global model
    tokenizer = AutoTokenizer.from_pretrained('stabilityai/stablelm-zephyr-3b')
    model = AutoModelForCausalLM.from_pretrained(
        'stabilityai/stablelm-zephyr-3b',
        device_map="auto"
    )
    done_load_model = time.time()  
    # log("[model] Done loading model: " + str(done_load_model - start))

async def zephyr(content: str) -> str:
    start = time.time()

    prompt = [{'role': 'user', 'content': prompt_constructor(content)}]
    inputs = tokenizer.apply_chat_template(
        prompt,
        add_generation_prompt=True,
        return_tensors='pt'
    )

    tokens = model.generate(
        inputs.to(model.device),
        max_new_tokens=get_max_length(content),
        temperature=0.01,
        do_sample=True
    )
    output = tokenizer.decode(tokens[0], skip_special_tokens=False)
    done_inference = time.time()
    # log("[model] Done loading inference: " + str(done_inference - start))
    return output

async def preload_stable_lm_chat_1_6b():
    start = time.time()

    global tokenizer
    global model
    tokenizer = AutoTokenizer.from_pretrained('stabilityai/stablelm-2-1_6b-chat')
    model = AutoModelForCausalLM.from_pretrained(
        'stabilityai/stablelm-2-1_6b-chat',
        device_map="auto",
    )
    done_load_model = time.time()
    # log("[model] Done loading model: " + str(done_load_model - start))

async def stable_lm_chat_1_6b(content:str) -> str:
    start = time.time()
    
    tokens = tokenizer.encode(prompt_constructor(content), truncation=True, max_length=2048)
    truncated_content = tokenizer.decode(tokens, skip_special_tokens=True)
    
    prompt = [{'role': 'user', 'content': truncated_content}]
    # print(prompt)
    inputs = tokenizer.apply_chat_template(
        prompt,
        add_generation_prompt=True,
        return_tensors='pt'
    )

    tokens = model.generate(
        inputs.to(model.device),
        max_new_tokens=get_max_length(content),
        temperature=0.01,
        do_sample=True
    )

    output = tokenizer.decode(tokens[:, inputs.shape[-1]:][0], skip_special_tokens=False)
    done_inference = time.time()
    # log("[model] Done loading inference: " + str(done_inference - start))
    # print(output)
    return output.rstrip("<|im_end|>\n<|endoftext|>")

async def preload_bart_large_cnn():
    start = time.time()
    global summarizer
    global model
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    done_load_model = time.time()
    # log("[model] Model loading time: " + str(done_load_model - start))

async def bart_large_cnn(content:str) -> str:
    start = time.time()
    
    tokenizer = summarizer.tokenizer
    tokens = tokenizer.encode(prompt_constructor(content), truncation=True, max_length=1024)
    truncated_content = tokenizer.decode(tokens, skip_special_tokens=True)
    
    # print(truncated_content)
    
    output = summarizer(
        truncated_content,
        max_length=2048,
        min_length=30,
        do_sample=False
    )
    done_inference = time.time()
    # log("[model] Done loading inference: " + str(done_inference - start))
    # print(output)
    return output[0]['summary_text']
    
async def preload_gemma_1_1_2b_it():
    start = time.time()
    global tokenizer
    global model
    tokenizer = AutoTokenizer.from_pretrained("google/gemma-1.1-2b-it", token=access_token)
    model = AutoModelForCausalLM.from_pretrained(
        "google/gemma-1.1-2b-it",
        torch_dtype=torch.bfloat16,
        # max_new_token=get_max_length(content),
        max_new_token=2048,
        token=access_token
    )
    done_load_model = time.time()
    # log("[model] Done loading model: " + str(done_load_model - start))

async def gemma_1_1_2b_it(content:str) -> str:
    start = time.time()
    
    input_text = prompt_constructor(content)
    input_ids = tokenizer(input_text, return_tensors="pt")
    
    # max_new_tokens=get_max_length(content),
    tokens = model.generate(
        **input_ids,
    )
    output = tokenizer.decode(tokens[0])

    done_inference = time.time()
    # log("[model] Done loading inference: " + str(done_inference - start))
    # print(output)
    return output

async def preload_falcon_ai_text_summarizer():
    start = time.time()
    global summarizer 
    summarizer = pipeline(
        "summarization", 
        model="Falconsai/text_summarization"
    )
    done_load_model = time.time()
    app.app.logger.info("[model] Done load model: " + str(done_load_model - start))

async def falcon_ai_text_summarizer(content:str) -> str:
    start = time.time()
    # asyncio.sleep(1)
    app.app.logger.info("Print here falcon")
    input = prompt_constructor(content)

    output = summarizer(
        input,
        max_length=get_max_length(content),
        min_length=30,
        do_sample=False)

    done_inference = time.time()
    app.app.logger.info("[model] Done inference: " + str(done_inference - start))
    result = output[0]['summary_text']
    return result.lstrip("Summarize the following segment into 1 sentence: ")


def main():
    # falcon_ai_text_summarizer(test_paragraph)
    # print(stable_lm_chat_1_6b(test_paragraph))
    # gemma_1_1_2b_it(test_paragraph)
    print(get_max_length(test_paragraph_1))
    preload_bart_large_cnn()
    bart_large_cnn(test_paragraph_1)
    
if __name__ == "__main__":
    main()