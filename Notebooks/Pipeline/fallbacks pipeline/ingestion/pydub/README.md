# 🛠️ Pydub Ingestion Fallback

This folder contains the Jupyter Notebook `ingestion_pydub.ipynb` which standardizes raw multi-format outreach audio files into a unified **16kHz mono 16-bit PCM WAV** file using the high-level pythonic `pydub` package.


### 💡 Easy Explanation (Plain English)

This method uses a popular Python library called `pydub` to load and convert your audio. It is like having a clean Python script open the audio, change its format, and save it. It's very easy to read and write, but it loads the whole audio file into memory, which might slow things down for very large files.

---


## ⚙️ Technical Working Principle

This method acts as a high-level Python object-oriented wrapper over FFmpeg. Here is how it functions:

1. **Audio Segment Ingestion**: `pydub.AudioSegment.from_file(path)` queries the underlying FFmpeg binary to read, decode, and load the entire audio stream into Python RAM as a raw sample array.
2. **Frame Rate Resampling (`.set_frame_rate(16000)`)**: Pydub applies a resampling filter over the loaded samples, restructuring the array density to represent exactly 16000 samples per second.
3. **Channel Downmixing (`.set_channels(1)`)**: Pydub combines multi-channel samples (stereo) by averaging adjacent frame data, downmixing the stream to a single channel.
4. **Serialization & Export**: The `export` method passes the transformed in-memory samples back to FFmpeg, encoding it using the `pcm_s16le` codec and packaging it inside a standard lossless `.wav` container.

---

## 📅 Step-by-Step Execution Guide

Follow these steps to run the notebook:

1. **Step 1: Install Dependencies**
   - Run the setup cell to download the `ffmpeg` system binary (necessary for Pydub to decode/encode formats) and install the python package via `pip install pydub`.
2. **Step 2: Mount Google Drive**
   - Execute the Google Drive mount cell to authorize access to your Drive files.
3. **Step 3: Configure Parameters Form**
   - Set the variables in the parameter form:
     - **`input_audio_path`**: Path to your raw input recording.
     - **`output_audio_path`**: Path where the standardized WAV will be written.
4. **Step 4: Run Pydub Conversion**
   - Run the conversion cell. Pydub will load the file, apply the sample rate and channel filters in memory, and export the standardized WAV file.
