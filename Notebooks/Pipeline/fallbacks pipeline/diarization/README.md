# 🎙️ Speaker Diarization Fallback Suite

This directory contains the local, offline fallback execution notebooks and guides for the speaker diarization pipeline stage. All implementations are designed to run 100% locally in Google Colab without external API dependencies.

---

## 🚦 Fallback Method Matrix & Priority Ranking

When selecting a diarization fallback method, use the following priority rankings based on temporal accuracy and execution stability:

| Priority Rank | Fallback Method | Core Technology | Primary Strength | Key Limitation |
| :--- | :--- | :--- | :--- | :--- |
| **Rank 1** | **[WhisperX](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/diarization/whisperx/README.md)** | Pyannote + Forced Phoneme Alignment (Wav2Vec2) | • Word-level timestamp precision<br>• Zero segment overlaps | • High VRAM requirement (runs on GPU) |
| **Rank 2** | **[FunASR](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/diarization/funasr/README.md)** | Alibaba CAM++ Speaker Verification Model | • Lightweight model footprint<br>• Excellent on accented speech | • Primarily documented in Chinese |

---

## 📑 Directory & Notebook Mapping

Each method is hosted in its own subdirectory containing a dedicated configuration notebook and guide:

* 📁 **[whisperx/](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/diarization/whisperx/README.md)**
  - 📓 [diarization_whisperx.ipynb](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/diarization/whisperx/diarization_whisperx.ipynb)
* 📁 **[funasr/](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/diarization/funasr/README.md)**
  - 📓 [diarization_funasr.ipynb](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/diarization/funasr/diarization_funasr.ipynb)

---

## ⚙️ General Operational Flow

All notebooks share a standardized layout for seamless interoperability:

1. **Environment Setup**: Installs the required libraries via `pip` (e.g. `whisperx`, `funasr`, `speechbrain`).
2. **Google Drive Mount**: Connects the Colab environment to your Google Drive.
3. **Form-Based Configuration**: Allows inputting paths via the Colab GUI fields:
   - `input_audio_path`: The standardized WAV file (16kHz mono).
   - `output_json_path`: Location where the diarized timeline JSON should be exported.
4. **Execution & Export**: Loads the model, infers speaker boundaries, and outputs a formatted timeline JSON:
   ```json
   [
       {
           "time": "[00:15 - 00:32]",
           "speaker": "SPEAKER_01",
           "text": ""
       }
   ]
   ```
