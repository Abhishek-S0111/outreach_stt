# YADEP: YouTube Audio Dataset Extraction Pipeline
### Summer Internship Warm-up Project at Annam.ai, IIT Ropar


YADEP is an end-to-end data pipeline to compile machine learning audio-text datasets from YouTube videos or playlists. It is optimized to bypass YouTube throttling and prevent Out-Of-Memory (OOM) crashes during transcription.

---

## 🚀 Key Features
- **Anti-Throttling**: Emulates client players to bypass YouTube rate-limiting.
- **Memory-Guarded Transcription**: Splits audio into 30-second frames to prevent OOM crashes during Whisper inference.
- **ML Ready**: Prepares dataset manifests and audio-to-text segments ready for model fine-tuning (STT/TTS).

---

## 📂 Folder Structure

```text
Kali's Previous work/
├── data/              # Output dataset CSV manifests (metadata, chunks, etc.)
├── docs/              # About the pipeline presentation and reports
├── notebooks/         # Colab execution and dataset cleaning notebooks
└── sample_outputs/    # Example processed audio and transcripts
```

---

## ⚙️ How it Works
1. **Input & Metadata Extraction**: Ingests YouTube URLs, validates length, and filters duplicates.
2. **Audio Acquisition & Slicing**: Downloads audio as `audio.mp3` and segments it into 30-second frames.
3. **Whisper Transcription**: Transcribes chunks using `openai/whisper-large-v3` with optimized GPU memory usage.
4. **Dataset Compilation**: Exports transcripts in `.txt` / `.json` / timestamp formats and generates final ML-ready CSV manifests.
