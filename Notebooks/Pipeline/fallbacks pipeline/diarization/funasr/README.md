# 🛠️ Speaker Diarization: FunASR (CAM++ SV)

Performs speaker diarization using Alibaba's open-source FunASR toolkit and the optimized CAM++ speaker verification embedding model.


### 💡 Easy Explanation (Plain English)

This method uses a lightweight Chinese speech model (from Alibaba) to group different speakers. It is very good at handling accented speech and doesn't require a lot of computing power, though most of its documentation is in Chinese.

---


## 🚦 Fallback Priority & Selection

- **Priority Rank**: **Rank 2**
- **Ranking Rationale**: CAM++ is a highly optimized, lightweight speaker verification architecture that delivers excellent accuracy and extremely fast inference speeds on accented speech data.

---

## ⚙️ Technical Working Principle

This fallback execution runs entirely **offline and locally** inside Google Colab.

### How it works:
1. **Drive Mount**: Connects to Google Drive to access standardization outputs.
2. **Standard Audio Input**: Reads the resampled 16kHz mono WAV file from the configured Drive path.
3. **Core Processing**: Initializes the `funasr` pipeline and extracts/clusters speaker turns.
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
