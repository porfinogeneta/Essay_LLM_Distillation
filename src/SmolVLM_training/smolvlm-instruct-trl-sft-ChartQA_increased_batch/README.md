---
base_model: HuggingFaceTB/SmolVLM-Instruct
library_name: transformers
model_name: smolvlm-instruct-trl-sft-ChartQA_increased_batch
tags:
- generated_from_trainer
- trl
- sft
licence: license
---

# Model Card for smolvlm-instruct-trl-sft-ChartQA_increased_batch

This model is a fine-tuned version of [HuggingFaceTB/SmolVLM-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-Instruct).
It has been trained using [TRL](https://github.com/huggingface/trl).

## Quick start

```python
from transformers import pipeline

question = "If you had a time machine, but could only go to the past or the future once and never return, which would you choose and why?"
generator = pipeline("text-generation", model="szymmon/smolvlm-instruct-trl-sft-ChartQA_increased_batch", device="cuda")
output = generator([{"role": "user", "content": question}], max_new_tokens=128, return_full_text=False)[0]
print(output["generated_text"])
```

## Training procedure

 


This model was trained with SFT.

### Framework versions

- TRL: 0.14.0
- Transformers: 4.48.2
- Pytorch: 2.6.0
- Datasets: 3.2.0
- Tokenizers: 0.21.0

## Citations



Cite TRL as:
    
```bibtex
@misc{vonwerra2022trl,
	title        = {{TRL: Transformer Reinforcement Learning}},
	author       = {Leandro von Werra and Younes Belkada and Lewis Tunstall and Edward Beeching and Tristan Thrush and Nathan Lambert and Shengyi Huang and Kashif Rasul and Quentin Gallouédec},
	year         = 2020,
	journal      = {GitHub repository},
	publisher    = {GitHub},
	howpublished = {\url{https://github.com/huggingface/trl}}
}
```