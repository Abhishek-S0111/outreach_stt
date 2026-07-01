# 🎙️ Noise Suppression & Separation Fallback

This folder contains local, offline fallback execution notebooks and guides for the noise suppression and audio separation pipeline stage. All implementations are designed to clean background noise and transient interferences from outreach audio.

---

## 🚦 Fallback Method Matrix & Priority Ranking

| Priority Rank | Fallback Method | Core Technology | Primary Strength | Key Limitation |
| :--- | :--- | :--- | :--- | :--- |
| **Rank 1** | **[deepfilternet](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/separation/deepfilternet/README.md)** | Rust Deep Filtering | • Removes transient noise/reverb<br>• Fast CPU execution | • Higher initial package installation |
| **Rank 2** | **[rnnoise](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/separation/rnnoise/README.md)** | Mozilla GRU Engine | • Extremely lightweight<br>• Highly voice-optimized | • Requires C compilation setup |

---

## 📑 Directory & Notebook Mapping

* 📁 **[deepfilternet/](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/separation/deepfilternet/README.md)**
  - 📓 [separation_deepfilternet.ipynb](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/separation/deepfilternet/separation_deepfilternet.ipynb)
* 📁 **[rnnoise/](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/separation/rnnoise/README.md)**
  - 📓 [separation_rnnoise.ipynb](file:///Users/mybook/Downloads/SOPHOMORE/GIT/outreach_stt/Notebooks/Pipeline/fallbacks%20pipeline/separation/rnnoise/separation_rnnoise.ipynb)
