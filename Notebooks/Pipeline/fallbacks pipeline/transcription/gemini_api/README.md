# 🛠️ Gemini API Transcription Fallback

This folder contains the Jupyter Notebook `transcription_gemini_api.ipynb` which transcribes standardized outreach audio files using the Gemini API's native multi-modal audio understanding capabilities.


### 💡 Easy Explanation (Plain English)

This method sends your audio file to Google's Gemini AI in the cloud to be transcribed. Gemini listens to the whole audio and writes down what is said. It gives highly accurate results and is very easy to use, but requires an internet connection and a Gemini API Key.

---


## ⚙️ Technical Working Principle

This method runs entirely as a cloud API fallback using the `google-generativeai` SDK. Here is how it functions:

1. **API Authentication**: Retrieves the `GEMINI_API_KEY` dynamically from the Google Colab environment secrets (`userdata.get`) to avoid hardcoded credentials.
2. **File Upload**: Uploads the standardized WAV file from your Google Drive path to Gemini's remote file storage via `genai.upload_file`.
3. **Multi-Modal ASR**: Passes the remote file reference directly to `gemini-1.5-flash` along with a transcription instructions prompt. Gemini processes the raw audio waveform using its native audio context window (zero-shot zero-segmentation).
4. **Verbatim Output**: Extracts the transcribed text directly and writes it to a `.txt` file on your Google Drive.
5. **Storage Cleanup**: Calls `audio_file.delete()` to ensure no residual files remain in the temporary Gemini API upload space.

---

## 📅 Step-by-Step Execution Guide

1. **Step 1: Install google-generativeai SDK**
   - Run the setup cell in the notebook to install the Google GenAI library.
2. **Step 2: Mount Google Drive**
   - Authorize file stream access by running the Colab mount cell.
3. **Step 3: Setup Secrets**
   - Save your API key in Google Colab Secrets (the key icon in the left sidebar) with the name **`GEMINI_API_KEY`**.
4. **Step 4: Configure Paths Form**
   - Fill out the variable paths:
     - **`input_audio_path`**: Path to your resampled 16kHz mono WAV file.
     - **`output_txt_path`**: Path to save the final text transcript.
5. **Step 5: Run Transcription**
   - Execute the processing cell. The notebook will upload the audio, request transcription, save the output, and clean up remote storage.
