# 🎙️ Audio Transcription Fallback

This folder contains local fallback execution notebooks and guides for the audio transcription pipeline stage. All implementations are designed to transcribe standardized audio waveforms using cloud endpoints.

---

## 🚦 Fallback Method Matrix & Priority Ranking

| Priority Rank | Fallback Method | Core Technology | Primary Strength | Key Limitation |
| :--- | :--- | :--- | :--- | :--- |
| **Rank 1** | **[gemini_api](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/transcription/gemini_api/README.md)** | Gemini Multi-Modal ASR | • Native audio context window<br>• Highest transcription fidelity | • Requires GEMINI_API_KEY |
| **Rank 2** | **[sarvam_api](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/transcription/sarvam_api/README.md)** | Sarvam Indian STT Model | • Optimized for Hindi and Punjabi speech | • Requires SARVAM_API_KEY |

---

## 📑 Directory & Notebook Mapping

* 📁 **[gemini_api/](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/transcription/gemini_api/README.md)**
  - 📓 [transcription_gemini_api.ipynb](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/transcription/gemini_api/transcription_gemini_api.ipynb)
* 📁 **[sarvam_api/](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/transcription/sarvam_api/README.md)**
  - 📓 [transcription_sarvam_api.ipynb](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/transcription/sarvam_api/transcription_sarvam_api.ipynb)
