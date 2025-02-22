# -*- coding: utf-8 -*-
"""Code Summarization.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S1vrZDuWR9HK9mre-o3kMZV7fClTbVBH
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install datasets
# import torch
# from datasets import Dataset, load_dataset
# from tqdm import tqdm

# device = torch.device('cuda')

dataset = Dataset.load_from_disk('./drive/MyDrive/React_dataset/EddieChen/')
dataset = load_dataset('EddieChen372/react_repos')['train'].remove_columns(['path','repo_name'])

from transformers import RobertaTokenizer, T5ForConditionalGeneration
model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-base-multi-sum')
model = model.to(device)
tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base-multi-sum')

def generate_labels(code):
  input_ids = tokenizer(code, return_tensors="pt").input_ids
  # input_ids = input_ids.to(device)
  generated_ids = model.generate(input_ids, max_length=50)
  return tokenizer.decode(generated_ids[0], skip_special_tokens=True)

labels ={}
import json
for i in tqdm(range(20000,30000)):
  data = dataset['content'][i]
  if not len(data)<=512 :
    continue
  text = generate_labels(data)
  labels[i] = text
  if i%1000 == 0:
    with open(f'labels-{i}.json','w',encoding='UTF-8') as file:
      json.dump(labels,file)
    labels = {}
