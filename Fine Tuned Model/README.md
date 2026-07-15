---
library_name: peft
license: mit
base_model: openai/whisper-large-v3-turbo
tags:
- base_model:adapter:openai/whisper-large-v3-turbo
- lora
- transformers
model-index:
- name: whisper-large-v3-turbo-gurmukhi-lora
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# whisper-large-v3-turbo-gurmukhi-lora

This model is a fine-tuned version of [openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) on an unknown dataset.
It achieves the following results on the evaluation set:
- Loss: 1.6912

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 5e-05
- train_batch_size: 4
- eval_batch_size: 8
- seed: 42
- gradient_accumulation_steps: 8
- total_train_batch_size: 32
- optimizer: Use OptimizerNames.ADAMW_BNB with betas=(0.9,0.999) and epsilon=1e-08 and optimizer_args=No additional optimizer arguments
- lr_scheduler_type: linear
- lr_scheduler_warmup_steps: 100
- training_steps: 1000
- mixed_precision_training: Native AMP
- label_smoothing_factor: 0.1

### Training results

| Training Loss | Epoch  | Step | Validation Loss |
|:-------------:|:------:|:----:|:---------------:|
| 19.2302       | 0.4069 | 50   | 2.3483          |
| 16.1382       | 0.8138 | 100  | 2.0084          |
| 15.0314       | 1.2197 | 150  | 1.8724          |
| 14.5433       | 1.6267 | 200  | 1.8118          |
| 13.9557       | 2.0326 | 250  | 1.7802          |
| 14.0038       | 2.4395 | 300  | 1.7612          |
| 13.9163       | 2.8464 | 350  | 1.7460          |
| 13.7943       | 3.2523 | 400  | 1.7359          |
| 13.6503       | 3.6592 | 450  | 1.7269          |
| 13.5450       | 4.0651 | 500  | 1.7190          |
| 13.4929       | 4.4720 | 550  | 1.7140          |
| 13.4390       | 4.8789 | 600  | 1.7090          |
| 13.5675       | 5.2848 | 650  | 1.7042          |
| 13.4880       | 5.6918 | 700  | 1.7008          |
| 13.2943       | 6.0977 | 750  | 1.6979          |
| 13.5647       | 6.5046 | 800  | 1.6958          |
| 13.3725       | 6.9115 | 850  | 1.6939          |
| 13.3143       | 7.3174 | 900  | 1.6925          |
| 13.4461       | 7.7243 | 950  | 1.6915          |
| 13.3344       | 8.1302 | 1000 | 1.6912          |


### Framework versions

- PEFT 0.18.1
- Transformers 5.0.0
- Pytorch 2.10.0+cu128
- Datasets 4.8.5
- Tokenizers 0.22.2