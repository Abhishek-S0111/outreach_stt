# 🛠️ FFmpeg CLI Ingestion Fallback

This folder contains the Jupyter Notebook `ingestion_ffmpeg_cli.ipynb` which standardizes raw multi-format outreach audio files into a unified **16kHz mono 16-bit PCM WAV** file using the system's compiled `ffmpeg` CLI binary.


### 💡 Easy Explanation (Plain English)

Think of this method as using a powerful system tool (`ffmpeg`) to convert and resize your audio files. It is like running a fast command-line app behind the scenes to make sure your audio is in the exact format (16kHz mono WAV) needed for transcription. It is extremely fast and doesn't use up your computer's memory.

---


## ⚙️ Technical Working Principle

This method runs at the OS level by launching a compiled FFmpeg binary inside a Python subprocess. Here is how it functions:

1. **Subprocess Spawning**: Python's `subprocess.run` command executes a shell command, spawning FFmpeg as an independent C-based process. This bypasses Python's Global Interpreter Lock (GIL) and runs at maximum native speed.
2. **Audio Decoding**: FFmpeg reads the headers of the input file (`input_audio_path`), automatically detects the codec (MP3, M4A, OGG, AAC), and decodes the compressed bitstream.
3. **Resampling Filter (`-ar 16000`)**: FFmpeg passes the decoded audio samples through its audio resampler filter, interpolating or decimating sample rates to exactly 16000Hz.
4. **Channel Downmixing (`-ac 1`)**: If the input audio has multiple channels (stereo), FFmpeg averages the left and right channel arrays into a single mono channel.
5. **Bit-Depth Casting (`-c:a pcm_s16le`)**: The samples are serialized using a Signed 16-bit Little-Endian Pulse Code Modulation (PCM) codec, matching Pyannote's training guidelines.
6. **Lossless WAV Packaging**: Writes the header chunks and raw PCM samples to a standard Waveform Audio File Format container on disk.

---

## 📅 Step-by-Step Execution Guide

Follow these steps to run the notebook:

1. **Step 1: Install System Dependencies**
   - Run the setup cell in the notebook. It runs `apt-get install -y ffmpeg` to ensure the FFmpeg binary is compiled and available in Colab's Linux container path.
2. **Step 2: Mount Google Drive**
   - Run the mounting block which calls `drive.mount('/content/drive')` to load your audio files and authorize file writing back to Drive.
3. **Step 3: Parameter Configuration Form**
   - Fill out the parameter fields in the Colab form:
     - **`input_audio_path`**: Path to your raw audio (e.g. `/content/drive/MyDrive/.../sample.m4a`).
     - **`output_audio_path`**: Path where the resampled WAV file will be saved.
4. **Step 4: Execute Conversion Subprocess**
   - Run the final cell. It constructs the FFmpeg command list, executes it, and verifies successful completion.
