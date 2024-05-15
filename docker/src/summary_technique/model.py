from transformers import AutoTokenizer, TFAutoModel, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
import time
import torch
from nltk import word_tokenize

test_paragraph = "After we follow accretion in the MAB during the first 5 Myr of the solar system's history, it is necessary to account for the various processes that happened during subsequent 4.5 Gyr evolution after gas disk dispersal. Specifically, the giant planet instability has been found to heavily deplete the MAB In this work, we consider the MAB region to be delimited as follows (e.g., We then use this MAB definition to select objects from the Minor Planet Center (MPC) databaseFigure For our depletion analysis, we further divide the MAB definition above into 5 sub-regions: Extended inner Main Belt (EiMB; a < 2.1 au), Inner Main Belt (IMB; 2.1 au < a < 2.5 au), Center Main Belt (CMB; 2.5 au < a < 2.82 au), Outer Main Belt (OMB; 2.82 au < a < 3.25 au), and Extended outer Main Belt (EoMB; a > 3.25 au). The row labeled D18 D f ac in Table . D f ac effectively reports the survival fraction of objects from the simulation. Yet, we prefer to refer to them as a depletion factor as those are the numbers we directly multiply the evolved population in order to account for their depletion. Dper is for the percentage of depletion Dper \u2248 100 \u00d7 (1 -D f ac ). Labels all and AM D JS P S /P J are for different cuts in the data by \u2022 C19 all refers to results taken from \u2022 C19 AM DJS P S /P J is also for results from The work by Our analyses clearly demonstrate that MAB depletion during the giant planet instability is not uniform. The fact that different MAB sub-regions have different depletion factors was first pointed out by"
access_token = "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"

def prompt_constructor(content:str) -> str:
    result = 'Summarize the following segment into 1 sentence: ' + content
    return result

def get_max_length(content:str) -> int:
    tokens = word_tokenize(content)
    return len(tokens)

def zephyr(content: str) -> str:
    start = time.time()
    tokenizer = AutoTokenizer.from_pretrained('stabilityai/stablelm-zephyr-3b')
    model = AutoModelForCausalLM.from_pretrained(
        'stabilityai/stablelm-zephyr-3b',
        device_map="auto"
    )
    done_load_model = time.time()

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
    print("Done loading model: " + str(done_load_model - start))
    print("Done loading inference: " + str(done_inference - start))
    return output

def stable_lm_chat_1_6b(content:str) -> str:
    start = time.time()
    tokenizer = AutoTokenizer.from_pretrained('stabilityai/stablelm-2-1_6b-chat')
    model = AutoModelForCausalLM.from_pretrained(
        'stabilityai/stablelm-2-1_6b-chat',
        device_map="auto",
    )
    done_load_model = time.time()
    # prompt = [{'role': 'user', 'content': 'Implement snake game using pygame'}]
    prompt = [{'role': 'user', 'content': prompt_constructor(content)}]
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
    print("Done loading model: " + str(done_load_model - start))
    print("Done loading inference: " + str(done_inference - start))
    # print(output)
    return output

def bart_large_cnn(content:str) -> str:
    start = time.time()
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    done_load_model = time.time()
    output = summarizer(
        prompt_constructor(content),
        max_length=get_max_length(content),
        min_length=30,
        do_sample=False
    )
    done_inference = time.time()
    print("Done loading model: " + str(done_load_model - start))
    print("Done loading inference: " + str(done_inference - start))
    print(output)
    return output
    
def gemma_1_1_2b_it(content:str) -> str:
    start = time.time()
    # quantization_config = BitsAndBytesConfig(load_in_8bit=True)

    tokenizer = AutoTokenizer.from_pretrained("google/gemma-1.1-2b-it", token=access_token)
    model = AutoModelForCausalLM.from_pretrained(
        "google/gemma-1.1-2b-it",
        torch_dtype=torch.bfloat16,
        max_length=get_max_length(content),
        token=access_token
    )
    done_load_model = time.time()
    # input_text = "Write me a poem about Machine Learning."
    input_text = prompt_constructor(content)
    # input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")
    input_ids = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**input_ids)
    output = tokenizer.decode(outputs[0])
    done_inference = time.time()
    print("Done loading model: " + str(done_load_model - start))
    print("Done loading inference: " + str(done_inference - start))
    # print(output)
    return output

def falcon_ai_text_summarizer(content:str) -> str:
    start = time.time()

    summarizer = pipeline("summarization", model="Falconsai/text_summarization")

    done_load_model = time.time()

    input = prompt_constructor(content)

    output = summarizer(
        input,
        max_length=get_max_length(content),
        min_length=30,
        do_sample=False)

    done_inference = time.time()
    print("Done load model: " + str(done_load_model - start))
    print("Done load model: " + str(done_inference - start))
    return output


def main():
    falcon_ai_text_summarizer()
    
if __name__ == "__main__":
    main()