# 🎙️ Audio Ingestion & Standardization Fallback

This folder contains local, offline fallback execution notebooks and guides for the audio ingestion and standardization pipeline stage. All implementations are designed to convert multi-format input audio into a standardized **16kHz mono 16-bit PCM WAV** file.

---

## 🚦 Fallback Method Matrix & Priority Ranking

| Priority Rank | Fallback Method | Core Technology | Primary Strength | Key Limitation |
| :--- | :--- | :--- | :--- | :--- |
| **Rank 1** | **[ffmpeg_cli](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/ingestion/ffmpeg_cli/README.md)** | Subprocess FFmpeg binary | • Exceptionally fast (compiled C)<br>• Zero Python memory overhead | • Requires compiled system binary |
| **Rank 2** | **[pydub](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/ingestion/pydub/README.md)** | High-level AudioSegment wrapper | • Clean Pythonic syntax<br>• Automated container parsing | • Loads entire file into RAM |

---

## 📑 Directory & Notebook Mapping

* 📁 **[ffmpeg_cli/](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/ingestion/ffmpeg_cli/README.md)**
  - 📓 [ingestion_ffmpeg_cli.ipynb](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/ingestion/ffmpeg_cli/ingestion_ffmpeg_cli.ipynb)
* 📁 **[pydub/](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/ingestion/pydub/README.md)**
  - 📓 [ingestion_pydub.ipynb](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/ingestion/pydub/ingestion_pydub.ipynb)
