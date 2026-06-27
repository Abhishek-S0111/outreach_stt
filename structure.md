# Repository Structure

```text
outreach_stt/
├── .gitignore
├── LICENSE
├── README.md
├── STT Architecture.png
│
├── Notebooks/
│   ├── Helper_Notebooks/
│   │   ├── Fine Tuning Script/                # Whisper fine-tuning notebooks
│   │   │   ├── Kaggle_whisper_medium_finetune.ipynb
│   │   │   ├── Kaggle_whisper_turbo_finetune.ipynb
│   │   │   ├── Whisper_small_LORA_finetune.ipynb
│   │   │   ├── whisper-finetune-Fixed.ipynb
│   │   │   ├── whisper-finetune-kaggle.ipynb
│   │   │   ├── whisper-finetune-large.ipynb
│   │   │   ├── whisper-finetune-turbo.ipynb
│   │   │   ├── whisper-medium-updated (1).ipynb
│   │   │   └── whisper-turbo-latest (1).ipynb
│   │   │
│   │   └── Transcription Notebooks/           # Transcription and script conversion notebooks
│   │       ├── Gemini/
│   │       │   └── Gurmukhi-Devanagari Dual-Script Transcription Workflow.ipynb
│   │       ├── Gemma/
│   │       │   ├── Gemma_4_12B_Multimodal_ASR.ipynb
│   │       │   └── Whisper_and_Gemma_4_12B_ASR_Pipeline.ipynb
│   │       └── transcription results/         # Evaluation reports and outputs
│   │           ├── Using Gemini Models/
│   │           │   ├── AUD-20260402-WA0018/
│   │           │   ├── Full Narration_MarauliKhurad/
│   │           │   ├── MarauliKhurad1/
│   │           │   ├── MarauliKhurad2/
│   │           │   └── MarauliKhurad3/
│   │           ├── whisper-medium/
│   │           └── whisper-turbo/
│   │
│   ├── Intermediate Pipeline Notebooks/       # Ingestion, noise reduction, and diarization modules
│   │   ├── Diarization Implementation NoteBook/
│   │   ├── Noise Suppression And Diarization/
│   │   ├── Noise_Suppression_Diarization_Splitting_Gemini_API/
│   │   ├── Noise_Suppression_Diarization_Splitting_Local_Whisper_LoRA/
│   │   └── Noisesuppression/
│   │
│   └── Pipeline/                              # Final active speech processing pipeline
│       ├── pipeline.ipynb
│       └── README.md
│
└── Previous Work/                             # Reorganized intern warm-up logs
    ├── Abhishek/
    │   ├── Audio and Transcript Extraction Pipeline/
    │   └── SLM Benchmarking/
    ├── Kali/
    │   └── Audio and Transcript Extraction Pipeline/
    │       ├── data/
    │       ├── docs/
    │       ├── notebooks/
    │       └── sample_outputs/
    └── Akshay/
        └── Audio and Transcript Extraction Pipeline/
```
