# Benchmark Report: Reference-Free Transcription Evaluation

## 1. Objective & Core Research Problem
When evaluating Automatic Speech Recognition (ASR) systems on production domains or unique localized telemetry datasets, human-verified ground-truth transcripts are often unavailable. Standard Word Error Rate (WER) metrics cannot execute without a verified reference text baseline.

This report presents a reference-free alternative benchmark strategy by establishing a **Cross-Model Consensus Framework** utilizing 5 discrete team-fine-tuned Whisper model configurations.

## 2. Benchmark Methodology
Instead of validating accuracy against an absolute static human script, transcription reliability is measured via **Majority Voting (Token-Level Consensus)**:
1. **Inference Execution:** The same target file (`Full Narration_MarauliKhurad.m4a`) is processed independently by all 5 LoRA architectures using identical decoding parameters ($16\text{ kHz}$ chunked stream processing, Punjabi localization).
2. **Pseudo-Ground Truth Construction:** A structural consensus vector is synthesized dynamically. For every sequential word slot ($i$), a token frequency matrix is evaluated. The word agreed upon by the majority of models is injected into the baseline reference string.
3. **Consensus WER (cWER) Evaluation:** Each individual model's original prediction stream is mapped against this artificial baseline using standard Levenshtein distance calculations. A lower **cWER** implies a model aligns closely with collective consensus, indicating higher operational stability and resistance to hallucination variations.

## 3. Benchmarking Matrix Results
The table below represents how closely each fine-tuned model variants adhere to the collective linguistic consensus:

| Model Name                                      |   Consensus WER (cWER) | Status                           |
|:------------------------------------------------|-----------------------:|:---------------------------------|
| Garden2006/whisper-large-v3-turbo-gurmukhi-lora |                 0.0688 | Evaluated via Cross-Model Voting |
| abhi8799/whisper-large-v3-turbo-gurmukhi-lora   |                 0.5888 | Evaluated via Cross-Model Voting |
| abhi8799/whisper-small-gurmukhi-lora            |                 0.8659 | Evaluated via Cross-Model Voting |
| KaliNangia/whisper-large-v3-turbo-gurmukhi-lora |                 0.6757 | Evaluated via Cross-Model Voting |
| KaliNangia/whisper-medium-gurmukhi-lora         |                 0.7346 | Evaluated via Cross-Model Voting |

## 4. Key Engineering Insights
* **Consensus Drivers:** Models with the lowest cWER scores demonstrate high vocabulary alignment with alternative parameter pools, marking them as stable candidate architectures for zero-shot tasks where a ground truth is missing.
* **Outlier Variance:** Higher cWER metrics flag architectures that display structural variations, alternative word order selections, or localized phrase interpretations.

---
*Report automatically compiled and generated in Google Colab.*
