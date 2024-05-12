from transformers import AutoTokenizer, TFAutoModel, AutoModelForCausalLM
import time

test_paragraph = "After we follow accretion in the MAB during the first 5 Myr of the solar system's history, it is necessary to account for the various processes that happened during subsequent 4.5 Gyr evolution after gas disk dispersal. Specifically, the giant planet instability has been found to heavily deplete the MAB In this work, we consider the MAB region to be delimited as follows (e.g., We then use this MAB definition to select objects from the Minor Planet Center (MPC) databaseFigure For our depletion analysis, we further divide the MAB definition above into 5 sub-regions: Extended inner Main Belt (EiMB; a < 2.1 au), Inner Main Belt (IMB; 2.1 au < a < 2.5 au), Center Main Belt (CMB; 2.5 au < a < 2.82 au), Outer Main Belt (OMB; 2.82 au < a < 3.25 au), and Extended outer Main Belt (EoMB; a > 3.25 au). The row labeled D18 D f ac in Table . D f ac effectively reports the survival fraction of objects from the simulation. Yet, we prefer to refer to them as a depletion factor as those are the numbers we directly multiply the evolved population in order to account for their depletion. Dper is for the percentage of depletion Dper \u2248 100 \u00d7 (1 -D f ac ). Labels all and AM D JS P S /P J are for different cuts in the data by \u2022 C19 all refers to results taken from \u2022 C19 AM DJS P S /P J is also for results from The work by Our analyses clearly demonstrate that MAB depletion during the giant planet instability is not uniform. The fact that different MAB sub-regions have different depletion factors was first pointed out by"

def prompt_constructor(content:str) -> str:
    result = 'Summarize the following segment into 1 sentence: ' + content
    return result

def zephyr():
    start = time.time()
    tokenizer = AutoTokenizer.from_pretrained('stabilityai/stablelm-zephyr-3b')
    model = AutoModelForCausalLM.from_pretrained(
        'stabilityai/stablelm-zephyr-3b',
        device_map="auto"
    )
    done_load_model = time.time()

    prompt = [{'role': 'user', 'content': 'List 3 synonyms for the word "tiny"'}]
    inputs = tokenizer.apply_chat_template(
        prompt,
        add_generation_prompt=True,
        return_tensors='pt'
    )

    tokens = model.generate(
        inputs.to(model.device),
        max_new_tokens=1024,
        temperature=0.01,
        do_sample=True
    )
    done_inference = time.time()
    print("Done loading model: " + str(done_load_model - start))
    print("Done loading inference: " + str(done_inference - start))
    print(tokenizer.decode(tokens[0], skip_special_tokens=False))

def stable_lm_chat_1_6b():
    start = time.time()
    tokenizer = AutoTokenizer.from_pretrained('stabilityai/stablelm-2-1_6b-chat')
    model = AutoModelForCausalLM.from_pretrained(
        'stabilityai/stablelm-2-1_6b-chat',
        device_map="auto",
    )
    done_load_model = time.time()
    # prompt = [{'role': 'user', 'content': 'Implement snake game using pygame'}]
    prompt = [{'role': 'user', 'content': prompt_constructor(test_paragraph)}]
    print(prompt)
    inputs = tokenizer.apply_chat_template(
        prompt,
        add_generation_prompt=True,
        return_tensors='pt'
    )

    tokens = model.generate(
        inputs.to(model.device),
        max_new_tokens=300,
        temperature=0.01,
        do_sample=True
    )
    output = tokenizer.decode(tokens[:, inputs.shape[-1]:][0], skip_special_tokens=False)
    done_inference = time.time()
    print("Done loading model: " + str(done_load_model - start))
    print("Done loading inference: " + str(done_inference - start))
    print(output)

def main():
    stable_lm_chat_1_6b()
    
if __name__ == "__main__":
    main()