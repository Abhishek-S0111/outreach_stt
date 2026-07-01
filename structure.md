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
│   │       │   ├── Gemini_Direct_Audio_Transcription_and_Insights.ipynb
│   │       │   ├── Gurmukhi-Devanagari Dual-Script Transcription Workflow.ipynb
│   │       │   └── README.md
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
│       ├── backup_fallback_strategies.md
│       ├── fallbacks pipeline/                # Local transcription reports for fallback pipeline
│       │   ├── diarization/
│       │   │   ├── diarizen/
│       │   │   │   ├── diarization_diarizen.ipynb
│       │   │   │   └── README.md
│       │   │   ├── funasr/
│       │   │   │   ├── diarization_funasr.ipynb
│       │   │   │   └── README.md
│       │   │   ├── speechbrain/
│       │   │   │   ├── diarization_speechbrain.ipynb
│       │   │   │   └── README.md
│       │   │   ├── wespeaker/
│       │   │   │   ├── diarization_wespeaker.ipynb
│       │   │   │   └── README.md
│       │   │   ├── whisperx/
│       │   │   │   ├── diarization_whisperx.ipynb
│       │   │   │   └── README.md
│       │   │   └── README.md
│       │   ├── ingestion/
│       │   │   ├── ffmpeg_cli/
│       │   │   │   ├── ingestion_ffmpeg_cli.ipynb
│       │   │   │   └── README.md
│       │   │   ├── pyav/
│       │   │   │   ├── ingestion_pyav.ipynb
│       │   │   │   └── README.md
│       │   │   ├── pydub/
│       │   │   │   ├── ingestion_pydub.ipynb
│       │   │   │   └── README.md
│       │   │   ├── scipy_wavefile/
│       │   │   │   ├── ingestion_scipy_wavefile.ipynb
│       │   │   │   └── README.md
│       │   │   ├── soundfile_scipy/
│       │   │   │   ├── ingestion_soundfile_scipy.ipynb
│       │   │   │   └── README.md
│       │   │   └── README.md
│       │   ├── refinement/
│       │   │   ├── intervaltree/
│       │   │   │   ├── refinement_intervaltree.ipynb
│       │   │   │   └── README.md
│       │   │   ├── networkx/
│       │   │   │   ├── refinement_networkx.ipynb
│       │   │   │   └── README.md
│       │   │   ├── pandas_grouping/
│       │   │   │   ├── refinement_pandas_grouping.ipynb
│       │   │   │   └── README.md
│       │   │   ├── pure_python/
│       │   │   │   ├── refinement_pure_python.ipynb
│       │   │   │   └── README.md
│       │   │   ├── spyder/
│       │   │   │   ├── refinement_spyder.ipynb
│       │   │   │   └── README.md
│       │   │   └── README.md
│       │   ├── separation/
│       │   │   ├── deepfilternet/
│       │   │   │   ├── separation_deepfilternet.ipynb
│       │   │   │   └── README.md
│       │   │   ├── rnnoise/
│       │   │   │   ├── separation_rnnoise.ipynb
│       │   │   │   └── README.md
│       │   │   ├── sox_cli/
│       │   │   │   ├── separation_sox_cli.ipynb
│       │   │   │   └── README.md
│       │   │   ├── spectral_subtraction/
│       │   │   │   ├── separation_spectral_subtraction.ipynb
│       │   │   │   └── README.md
│       │   │   ├── webrtc_vad/
│       │   │   │   ├── separation_webrtc_vad.ipynb
│       │   │   │   └── README.md
│       │   │   └── README.md
│       │   ├── splitting/
│       │   │   ├── ffmpeg_slicing/
│       │   │   │   ├── splitting_ffmpeg_slicing.ipynb
│       │   │   │   └── README.md
│       │   │   ├── pyav_demuxing/
│       │   │   │   ├── splitting_pyav_demuxing.ipynb
│       │   │   │   └── README.md
│       │   │   ├── pydub_slicing/
│       │   │   │   ├── splitting_pydub_slicing.ipynb
│       │   │   │   └── README.md
│       │   │   ├── scipy_slicing/
│       │   │   │   ├── splitting_scipy_slicing.ipynb
│       │   │   │   └── README.md
│       │   │   ├── soundfile_reading/
│       │   │   │   ├── splitting_soundfile_reading.ipynb
│       │   │   │   └── README.md
│       │   │   └── README.md
│       │   ├── transcription/
│       │   │   ├── gemini_api/
│       │   │   │   ├── transcription_gemini_api.ipynb
│       │   │   │   └── README.md
│       │   │   ├── sarvam_api/
│       │   │   │   ├── transcription_sarvam_api.ipynb
│       │   │   │   └── README.md
│       │   │   └── README.md
│       │   └── README.md
│       ├── pipeline.ipynb
│       ├── fallbacks_pipeline.ipynb
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
