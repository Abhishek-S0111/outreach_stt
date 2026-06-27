# Audio and Transcript Extraction Pipeline

This directory contains a notebook-based workflow for collecting YouTube audio, extracting speech data, and generating transcripts for downstream NLP and speech-processing tasks.

## Currently used for **Krishi Darshan YT Videos**  
Please modify according to own use. 

## Purpose

The pipeline is designed to:
- download audio from YouTube videos,
- organize raw and processed audio data,
- run transcription workflows using Whisper-based approaches,
- store sample transcripts for inspection and benchmarking.

## Folder Structure

- Helper_Notebooks/: supporting notebooks for downloading and preparing data.
- Notebooks/: main pipeline notebooks for dataset capture, audio extraction, and transcription.
- Sample_Transcripts/: example transcript outputs generated during experimentation.
- Testing_Notebooks/: exploratory and experimental notebooks.

## Main Notebooks

- YADEP_Phase1_Capture_Dataset.ipynb: captures or prepares the candidate video dataset.
- YADEP_Phase2_Extract_Audio.ipynb: downloads and extracts audio from the selected sources.
- YADEP_Phase3_Transcription(_Fetch_and_Whisper_).ipynb: runs transcription using available APIs or Whisper-based workflows.

## Setup

1. Create and activate a Python environment.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure FFmpeg is installed on the system and available in the PATH, since audio processing depends on it.

## Typical Workflow

1. Use the helper notebooks to inspect or download source videos.
2. Run the dataset capture notebook to define the input set.
3. Run the audio extraction notebook to obtain audio files.
4. Run the transcription notebook to generate transcripts.
5. Review the outputs in the Sample_Transcripts directory.

## Notes

- The repository includes both production-style notebooks and experimental notebooks.
- Some transcription approaches may require additional GPU or model-specific dependencies depending on the chosen backend.
- Transcripts and media outputs should be kept organized to support reproducible experiments.

## Dependencies

The main Python requirements include:
- yt-dlp
- pandas
- pydub
- youtube-transcript-api
- ffmpeg-python

Optional packages for heavier transcription workflows include:
- transformers
- torch
- whisper-jax
