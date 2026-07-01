# 🛠️ Speaker Diarization: WhisperX (Forced Alignment)

Performs word-level aligned speaker diarization using Pyannote segmentation and forced alignment models (like Wav2Vec2) locally.


### 💡 Easy Explanation (Plain English)

This method uses an advanced model to detect who is speaking and when. It does this by aligning the text of what is said with the audio at a word-by-word level. This gives extremely accurate timestamps without overlapping speakers, but it requires a graphics card (GPU) to run fast.

---


## 🚦 Fallback Priority & Selection

- **Priority Rank**: **Rank 1 (Primary Fallback Target)**
- **Ranking Rationale**: WhisperX offers the highest temporal resolution by aligning speaker turn boundaries down to the exact phoneme and word timestamps, making it the most robust offline diarization candidate.

---

## ⚙️ Technical Working Principle

This fallback execution runs entirely **offline and locally** inside Google Colab.

### How it works:
1. **Drive Mount**: Connects to Google Drive to access standardization outputs.
2. **Standard Audio Input**: Reads the resampled 16kHz mono WAV file from the configured Drive path.
3. **Core Processing**: Initializes the `whisperx` pipeline and extracts/clusters speaker turns.
4. **Target Export**: Saves the chronological timeline as a JSON array (`[ { "time": "[MM:SS - MM:SS]", "speaker": "SPEAKER_XX", "text": "" } ]`) back to Google Drive.

---

## 📅 Step-by-Step Execution Guide

1. **Step 1: Install Setup Packages**
   - Run the initial setup cell to download and install the required library packages.
2. **Step 2: Google Drive Mounting**
   - Execute the mounting cell to link Google Drive.
3. **Step 3: Setup Parameter Paths**
   - Enter your `input_audio_path` and `output_json_path` in the parameter form.
4. **Step 4: Execute Processing**
   - Run the final block to calculate the speaker turns and write out the timeline JSON.
