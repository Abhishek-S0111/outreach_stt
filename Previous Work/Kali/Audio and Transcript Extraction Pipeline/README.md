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
Audio and Transcript Extraction Pipeline/
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

---

## 📊 Pipeline Phase Flow Architecture

The data processing pipeline proceeds systematically across 12 discrete operational phases split into clear execution blocks:

### 1. Environment & Utility Provisioning
Installs core system binary decoders (`ffmpeg`), specific asset download layers (`yt-dlp`), sound processing wrappers (`pydub`), optimization packages (`accelerate`), and machine learning model backends (`transformers`, `torch`).

### 2. Input Gate Validation
Ingests a single YouTube Video or Playlist URL (`TARGET_URL`). Performs protective sanity checking to block invalid profile, channel, or creator landing pages.

### 3. Metadata Extraction Scanning
Executes high-velocity flat extraction sequences over the target URL index to gather core metrics (`Video ID`, `Title`, `Duration`, and `Uploader/Channel`) without activating heavy file-stream transfers.

### 4. Integrity Filtering & Alignment
Constructs the raw tracking spreadsheet (`YT_DATASET.csv`), executes column validation checks, purges corrupted or empty video descriptors, and runs a first-pass duplication filter using unique alphanumeric identifiers.

### 5. Workspace Isolation Setup
Filters out assets exceeding specified computational limits (e.g., maximum runtime thresholds like 30 minutes). Builds isolated workspace directories structured cleanly under a localized workspace repository namespace (`KrishiDarshan/<VIDEO_ID>`).

### 6. Bypassed Audio Acquisition
Deploys the upgraded Deno JS runtime engine wrapper to download master stream arrays and cleanly re-encodes structural components down to pristine standalone `audio.mp3` binary objects at standard bitrates.

### 7. Unified 30-Second Slicing Engine
Performs a storage verification pass to build the active asset manifest (`VERIFIED_AUDIO_INDEX.csv`). Re-loads localized master audio tracks via `pydub`, audits durations, and segments data structures sequentially into atomic 30-second frames (`chunk_000.mp3`, `chunk_001.mp3`, etc.).

### 8. Hardware Optimization Audit
Initiates system checks verifying active hardware acceleration arrays (e.g., Tesla T4 GPU engines), software library linkages (PyTorch, Hugging Face ecosystem), and binary paths (`ffmpeg`).

### 9. Memory-Guarded Speech Recognition (ASR)
Triggers custom garbage collection sweeps (`gc.collect`) and empties standard CUDA caches. Initializes `openai/whisper-large-v3` weights into half-precision matrices using memory-mapped allocations. Sequences through frames, filtering out fractured data elements (<15KB) to prevent matrix dimension exceptions, and exports linear transcript lines.

### 10. Multi-Format Output Multiplexer
Binds textual strings to assemble three specialized output configurations within individual video workspaces:
- `transcript.txt`: Standard plain-text output mapping for textual parsing.
- `transcript.json`: Comprehensive application package containing full extraction metadata, execution records, pipeline details, and transcribed assets.
- `transcript_timestamps.txt`: Aligned timeline representation tracking simulated step drift across 30-second window increments.

### 11. Quality Assurance Audit
Scans physical storage layout layers and compiles data into a comprehensive Markdown file (`QUALITY_AUDIT_REPORT.md`) outlining execution metrics, item exceptions, failed extractions, and tracking checks.

### 12. Final Machine Learning Matrix Compiler
Assembles and saves the definitive data deliverables across two key analytical tables:
- `FINAL_VIDEO_MANIFEST.csv`: High-level global map indexing durations, word counts, and paths for all produced master audio and transcript assets.
- `FINAL_ML_TRAINING_CHUNKS.csv`: Highly granular machine-learning-ready framework aligning segment ids, parent video maps, local audio chunk vectors, and targeted piece text values.

