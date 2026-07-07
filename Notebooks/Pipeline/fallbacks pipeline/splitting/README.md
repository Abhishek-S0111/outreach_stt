# 🎙️ Audio Splitting & Speaker Isolation Fallback

This folder contains local, offline fallback execution notebooks and guides for the audio splitting and speaker isolation pipeline stage. All implementations are designed to slice and isolate waveforms for each speaker's voice turns.

---

## 🚦 Fallback Method Matrix & Priority Ranking

| Priority Rank | Fallback Method | Core Technology | Primary Strength | Key Limitation |
| :--- | :--- | :--- | :--- | :--- |
| **Rank 1** | **[pydub_slicing](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/splitting/pydub_slicing/README.md)** | Pydub Slicing | • Simple pythonic array addition<br>• Handles overlapping turns | • High RAM footprint for large files |
| **Rank 2** | **[soundfile_reading](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/splitting/soundfile_reading/README.md)** | SoundFile Block Seek | • Memory efficient (reads from disk) | • Slower disk I/O reads |

---

## 📑 Directory & Notebook Mapping

* 📁 **[pydub_slicing/](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/splitting/pydub_slicing/README.md)**
  - 📓 [splitting_pydub_slicing.ipynb](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/splitting/pydub_slicing/splitting_pydub_slicing.ipynb)
* 📁 **[soundfile_reading/](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/splitting/soundfile_reading/README.md)**
  - 📓 [splitting_soundfile_reading.ipynb](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/splitting/soundfile_reading/splitting_soundfile_reading.ipynb)
