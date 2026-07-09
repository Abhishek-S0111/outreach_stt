# 🛠️ Sarvam API Transcription Fallback

This folder contains the Jupyter Notebook `transcription_sarvam_api.ipynb` which transcribes standardized outreach audio files using Sarvam AI's speech-to-text API (highly optimized for Indian languages, including Hindi and Punjabi).


### 💡 Easy Explanation (Plain English)

This method sends your audio to Sarvam AI's cloud service, which is specifically trained for Indian languages (like Hindi and Punjabi). It is excellent at transcribing regional dialects and accents, but requires an internet connection and a Sarvam API Key.

---


## ⚙️ Technical Working Principle

This method executes transcription using Sarvam AI's REST API. Here is how it functions:

1. **API Key Authentication**: Pulls the `SARVAM_API_KEY` from the Colab secrets and attaches it as an HTTP header: `"api-subscription-key": api_key`.
2. **Multipart/Form-Data Request**: Opens the local WAV file on-the-fly and sends it in a POST request payload along with metadata:
   - **`language_code`**: Set to `"pa-IN"` (Punjabi - India) or `"hi-IN"` (Hindi - India).
   - **`model`**: Set to `"saarika:v1"` (Sarvam's optimized multilingual STT model).
3. **API Processing**: Sarvam's servers decode the binary audio stream and apply deep acoustic models trained specifically on accented Indian language discussions.
4. **JSON Serialization**: Parses the resulting JSON response and exports the transcript verbatim to a text file on your Google Drive.

---

## 📅 Step-by-Step Execution Guide

1. **Step 1: Install Requests Library**
   - Run the initial cell to install standard python network request libraries.
2. **Step 2: Mount Google Drive**
   - Mount your Drive using the authentication cell.
3. **Step 3: Save API Key**
   - Save your subscription key in Google Colab Secrets under the name **`SARVAM_API_KEY`**.
4. **Step 4: Configure Parameters Form**
   - Fill in the form fields:
     - **`input_audio_path`**: Path to the standardized WAV.
     - **`output_txt_path`**: Target transcription text file.
     - **`language_code`**: Select `"pa-IN"` (for Punjabi) or `"hi-IN"` (for Hindi).
5. **Step 5: Execute POST Request**
   - Run the final cell to submit the request, parse the JSON transcript, and save it to Drive.
