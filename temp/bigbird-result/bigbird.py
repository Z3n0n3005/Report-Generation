from transformers import BigBirdPegasusForConditionalGeneration, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("google/bigbird-pegasus-large-arxiv")

# by default encoder-attention is `block_sparse` with num_random_blocks=3, block_size=64
model = BigBirdPegasusForConditionalGeneration.from_pretrained("google/bigbird-pegasus-large-arxiv")

# decoder attention type can't be changed & will be "original_full"
# you can change `attention_type` (encoder only) to full attention like this:
model = BigBirdPegasusForConditionalGeneration.from_pretrained("google/bigbird-pegasus-large-arxiv", attention_type="original_full")

# you can change `block_size` & `num_random_blocks` like this:
model = BigBirdPegasusForConditionalGeneration.from_pretrained("google/bigbird-pegasus-large-arxiv", block_size=16, num_random_blocks=2)

text = "Replace me by any text you'd like."
inputs = tokenizer(text, return_tensors='pt')
prediction = model.generate(**inputs)
prediction = tokenizer.batch_decode(prediction)