# 🛡️ Pipeline Step-Wise Backup & Fallback Strategies

This document serves as a comprehensive reference guide for engineering local, offline fallbacks, backups, and alternatives for each of the 6 core stages of the Outreach Speech-to-Text and Insights Pipeline. To maintain data privacy, local residency, and operate without internet connectivity, **all external APIs have been excluded** in favor of open-source local libraries and models.

---

## 🗺️ Pipeline Step Overview

```mermaid
graph LR
    Step1[1. Ingestion] --> Step2[2. Suppression]
    Step2 --> Step3[3. Diarization]
    Step3 --> Step4[4. Merging Turns]
    Step4 --> Step5[5. Splitting]
    Step5 --> Step6[6. Transcription]
```

---

## 1. Audio Ingestion & Standardization (16kHz Mono WAV)
*Objective: Read various audio formats (MP3, M4A, OGG, WAV) and resample them to a unified 16kHz, single-channel WAV format.*

| # | Fallback Method | Core Principle | Pros | Cons |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **FFmpeg CLI Subprocess** | Call compiled `ffmpeg` binary using python's `subprocess` library. | • High speed (C-based)<br>• Supports almost all audio containers<br>• Very low memory overhead | • Requires FFmpeg installed on the OS<br>• Parsing CLI error streams is fragile |
| **2** | **Pydub (AudioSegment)** | High-level wrapper over FFmpeg/Audioop. | • Clean, pythonic API<br>• Built-in format auto-detection | • Still requires backing FFmpeg binary<br>• Loads entire file into RAM |

---

## 2. Dynamic Noise Suppression
*Objective: Clean background noise, stationary hiss, and transient interferences from outreach audio recorded in open-air rural environments.*

| # | Fallback Method | Core Principle | Pros | Cons |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **DeepFilterNet** | Rust-based deep learning framework using deep filtering on CPU. | • Removes transient noise and reverb<br>• Real-time speed on single CPU thread | • Requires PyTorch and Rust-compiled package<br>• Slightly higher memory profile |
| **2** | **RNNoise (RNN Engine)** | Mozilla's recurrent neural network noise suppression library. | • Exceptionally lightweight<br>• Low latency | • Requires C compilation and `ctypes` bindings |

---

## 3. Speaker Diarization (Local & Offline)
*Objective: Identify "who spoke when" and cluster speaker turns into chronological segment timelines without utilizing cloud API endpoints.*

| # | Fallback Method | Core Principle | Pros | Cons |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **WhisperX (Forced Alignment)** | Performs phoneme-level forced alignment (via Wav2Vec2) to map speaker turns to exact words. | • SOTA word-level speaker timestamps<br>• Very clean speaker segment transition resolution | • Multi-model pipeline consumes substantial RAM/VRAM |
| **2** | **FunASR (CAM++ Embeddings)** | Alibaba's Speech Toolkit utilizing the CAM++ speaker embedding model for high-efficiency clustering. | • High accuracy on accented conversational speech<br>• Lightweight footprint | • Chinese documentation dominates community forums<br>• Harder to customize clustering parameters |

---

## 4. Merging Speaker Turns
*Objective: Consolidate segmented turns, merge adjacent turns by the same speaker, and calculate conversational statistics.*

| # | Fallback Method | Core Principle | Pros | Cons |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Vectorized Pandas Grouping** | Merge timelines using Pandas vectorized dataframe shifting and rolling windows. | • Extremely fast on large dataframes<br>• Clean code structure | • Pandas dataframe overhead for tiny files |
| **2** | **Pure Python List Accumulator** | Standard single-pass loop checking `current_start` against `prev_end`. | • Zero dependencies<br>• Highly portable code | • Can be slower for files with thousands of segments |

---

## 5. Audio Splitting & Speaker Isolation
*Objective: Extract individual turn waveforms or concatenate turns belonging to the same speaker to export isolated WAV files.*

| # | Fallback Method | Core Principle | Pros | Cons |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Pydub Waveform Slicing** | Slice and concatenate via Pydub AudioSegments (`audio[start_ms:end_ms]`). | • Simple operators (`+` to concatenate)<br>• In-memory processing | • High RAM usage for large audio files |
| **2** | **SoundFile Block Reading** | Read audio segments from disk block-by-block using `sf.SoundFile.read(frames=...)`. | • Low memory footprint (no need to load entire file) | • Slower sequential disk reads |

---

## 6. Transcription (Local & Offline)
*Objective: Transcribe speaker turns in Punjabi Gurmukhi/Devanagari, run local translations, and perform analysis without cloud APIs.*

| # | Fallback Method | Core Principle | Pros | Cons |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Faster-Whisper (CTranslate2)** | Run Whisper model compiled with CTranslate2 engine locally. | • Up to 4x faster than standard transformers<br>• Reduced VRAM footprint | • Cannot load custom LoRA weights natively without conversion |
| **2** | **Whisper.cpp (C/C++ Port)** | Run transcription using a compiled binary of Whisper.cpp. | • Extremely fast on CPU<br>• Zero Python dependency footprint | • Requires binary compilation on host system |
