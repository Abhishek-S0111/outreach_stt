"""
Audio Processing Module
Handles Audio Extraction (FFmpeg), Transcription (Whisper), and Translation (IndicTrans2)
"""
from pathlib import Path
from typing import Optional, Dict, List, Any
import ffmpeg
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForSpeechSeq2Seq, pipeline, AUtoProcessor
from config import settings
from src.core.utils import log
from peft import PeftModel, PeftConfig
import noisereduce as nr
import soundfile as sf
import librosa
import json
import os

# --- Part 1: Audio Extractor ---

class AudioExtractor:
    """Extract and normalize audio from video files"""
    
    @staticmethod
    async def extract_audio(video_path: Path, output_path: Optional[Path] = None, audio_format: str = "wav", sample_rate: int = 16000) -> Path:
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        output_path = output_path or video_path.parent / f"{video_path.stem}_audio.{audio_format}"
        try:
            log.info(f"Extracting audio from {video_path.name}")
            stream = ffmpeg.input(str(video_path))
            codec = 'pcm_s16le' if audio_format == 'wav' else 'libmp3lame'
            stream = ffmpeg.output(stream, str(output_path), acodec=codec, ar=sample_rate, ac=1)
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            log.info(f"Audio extracted: {output_path.name}")
            return output_path
        except ffmpeg.Error as e:
            err = e.stderr.decode() if e.stderr else str(e)
            log.error(f"FFmpeg error: {err}")
            raise RuntimeError(f"Audio extraction failed: {err}")

    @staticmethod
    async def normalize_audio(audio_path: Path, target_level: float = -20.0) -> Path:
        output_path = audio_path.parent / f"{audio_path.stem}_normalized{audio_path.suffix}"
        try:
            log.info(f"Normalizing audio: {audio_path.name}")
            stream = ffmpeg.input(str(audio_path))
            stream = ffmpeg.filter(stream, 'loudnorm', I=target_level)
            stream = ffmpeg.output(stream, str(output_path))
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            return output_path
        except ffmpeg.Error as e:
            log.error(f"Normalization failed: {e}")
            raise

    @staticmethod
    def get_audio_duration(audio_path: Path) -> float:
        try:
            return float(ffmpeg.probe(str(audio_path))['format']['duration'])
        except Exception as e:
            log.error(f"Error getting duration: {e}")
            return 0.0

    @staticmethod
    async def concat_audio_files(file_paths: List[Path], output_path: Path) -> Path:
        import asyncio, subprocess
        log.info(f"Concatenating {len(file_paths)} files into {output_path.name}")
        list_file = output_path.parent / "concat_list.txt"
        with open(list_file, "w") as f:
            for path in file_paths:
                f.write(f"file '{str(path.absolute()).replace("'", "'\\''")}'\n")
        
        cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-vn", "-acodec", "aac", str(output_path)]
        process = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {stderr.decode()}")
        
        log.info(f"Merged file created: {output_path}")
        return output_path


    """
        We need modules for noise suppresion.
    """

    @staticmethod
    async def load_audio(video_path:Path) -> list:
        import os
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Invalid Video Path: {video_path}\n ")
        
        try:
            y, sr = librosa.load(video_path, sr=None)
        except Exception as e:
            print(f"Following error was encountered while loading the file.: {e}")

        return [y,sr]

    @staticmethod
    async def noise_suppresion(video_path: Path) -> list:
        aud = AudioExtractor.load_audio(video_path)
        y = aud[0]
        sr = aud[1]

        try:
            y_denoised = nr.reduce_noise(y=y, sr=sr, stationary=False, prop_decrease=0.85)
        except Exception as e:
            print(f"The following error was encountered: {e}")

        output_path = video_path
        sf.write(output_path, y_denoised, sr)

    # """
    #     Audio Splits
    # """
    # #Source currently undecided 



    # @staticmethod
    # async def audio_splitting(audio_path:Path, refined_timeline_json_path: Path):
    #     audio_path = ""
    #     refined_timeline_json_path = ""
    #     isolated_output_folder = ""

    #     isolate_speaker_wise = True # @param {type:"boolean"}
    #     export_individual_turns = True # @param {type:"boolean"}

    #     if not os.path.exists(audio_path):
    #         print(f"[ERROR] Cleaned audio not found at: '{audio_path}'")
    #     elif not os.path.exists(refined_timeline_json_path):
    #         print(f"[ERROR] Refined timeline JSON not found at: '{refined_timeline_json_path}'")
    #     else:
    #         audio_filename = os.path.basename(audio_path)
    #         audio_name_only = audio_filename.replace("_cleaned.wav", "").replace(".wav", "")
    #         os.makedirs(isolated_output_folder, exist_ok=True)
    #         print(f"[SUCCESS] Validated paths. Isolated audio tracks will be saved in: {isolated_output_folder}")

    #     #1. Load refined timeline
    #     with open(refined_timeline_json_path, "r", encoding="utf-8") as f:
    #         speaker_segments = json.load(f)
            
    #     #Create specific folder for output files
    #     specific_isolated_folder = os.path.join(isolated_output_folder, audio_name_only)
    #     os.makedirs(specific_isolated_folder, exist_ok=True)
        
    #     #Load cleaned audio file
    #     print(f"Loading cleaned audio file for splitting: '{audio_path}'")
    #     y, sr = librosa.load(audio_path, sr=16000, mono=True)
        
    #     #Dictionary to hold samples for concatenating speaker-wise
    #     speaker_audio_data = {}
        
    #     #Time formatting helper for filenames: convert seconds to [MM-SS.d]
    #     def format_time_filename(seconds):
    #         hours = int(seconds // 3600)
    #         minutes = int((seconds % 3600) // 60)
    #         secs = int(seconds % 60)
    #         millis = int((seconds - int(seconds)) * 10)
    #         if hours > 0:
    #             return f"{hours:02d}-{minutes:02d}-{secs:02d}.{millis:01d}"
    #         else:
    #             return f"{minutes:02d}-{secs:02d}.{millis:01d}"
                
    #     #1. Process and extract segments
    #     for idx, entry in enumerate(speaker_segments):
    #         start_sec = entry['start']
    #         end_sec = entry['end']
    #         speaker = entry['speaker']
            
    #         # Calculate sample indices
    #         start_sample = int(start_sec * sr)
    #         end_sample = int(end_sec * sr)
            
    #         # Slice the audio array
    #         chunk = y[start_sample:end_sample]
            
    #         # Accumulate for speaker-wise isolation
    #         if speaker not in speaker_audio_data:
    #             speaker_audio_data[speaker] = []
    #         speaker_audio_data[speaker].append(chunk)
            
    #         # If user wants individual turns exported
    #         if export_individual_turns:
    #             turns_folder = os.path.join(specific_isolated_folder, "individual_turns", speaker)
    #             os.makedirs(turns_folder, exist_ok=True)
                
    #             start_str = format_time_filename(start_sec)
    #             end_str = format_time_filename(end_sec)
    #             turn_filename = f"{audio_name_only}_{speaker}_turn_{idx+1:03d}_{start_str}_to_{end_str}.wav"
    #             turn_filepath = os.path.join(turns_folder, turn_filename)
    #             sf.write(turn_filepath, chunk, sr)
                
    #     # 2. Export speaker-wise concatenated audio
    #     if isolate_speaker_wise:
    #         print("\n--- Exporting Concatenated Speaker-Wise Audio ---")
    #         for speaker, chunks in speaker_audio_data.items():
    #             if chunks:
    #                 # Concatenate all chunks for this speaker
    #                 concatenated_audio = np.concatenate(chunks)
    #                 speaker_filename = f"{audio_name_only}_{speaker}_isolated.wav"
    #                 speaker_filepath = os.path.join(specific_isolated_folder, speaker_filename)
    #                 sf.write(speaker_filepath, concatenated_audio, sr)
    #                 print(f"[SUCCESS] Exported isolated audio for {speaker} to '{speaker_filepath}'")
                    
    #     print(f"\n[SUCCESS] Audio splitting and speaker isolation complete! Output saved in: '{specific_isolated_folder}'")
     
"""
Audio Must be splitted based on the speakers speaking at the moment
"""




# --- Part 2: Transcription Service ---

class TranscriptionService:
    """Transcribe audio using Fine Tuned Whisper"""
    
    def __init__(self):
        self.model = None
        self.model_loaded = False
        
    def load_model(self):
        if not self.model_loaded:
            log.info(f"Loading Whisper model: {settings.whisper_finetuned_model}")
            try:
                

                self.model = WhisperModel(
                    settings.whisper_finetuned_model,
                    device=settings.whisper_device,
                    compute_type="int8" if settings.whisper_device == "cpu" else "float16"
                )
                self.model_loaded = True
                log.info("Whisper model loaded")
            except Exception as e:
                log.error(f"Failed to load Whisper: {e}")
                raise

    async def transcribe(self, audio_path: Path, language: Optional[str] = None) -> Dict[str, Any]:
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio not found: {audio_path}")
        self.load_model()
        
        try:
            log.info(f"Transcribing {audio_path.name}")
            lang_map = {"punjabi": "pa", "hindi": "hi", "english": "en"} # Add others as needed
            lang_code = lang_map.get(language.lower()) if language else None
            
            segments, info = self.model.transcribe(str(audio_path), language=lang_code, beam_size=5, vad_filter=True)
            
            full_text = []
            detailed = []
            for s in segments:
                full_text.append(s.text)
                detailed.append({"start": s.start, "end": s.end, "text": s.text.strip(), "confidence": s.avg_logprob})
            
            log.info(f"Transcription done. Lang: {info.language}")
            return {
                "text": " ".join(full_text).strip(),
                "language": info.language,
                "language_probability": info.language_probability,
                "duration": info.duration,
                "segments": detailed
            }
        except Exception as e:
            log.error(f"Transcription error: {e}")
            raise

# --- Part 3: Translation Service ---

class TranslationService:
    """Translate Indian languages to English"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        self.lang_codes = {
            "punjabi": "pan_Guru", "hindi": "hin_Deva", "english": "eng_Latn"
            # Add other mappings from original file if needed
        }

    def load_model(self):
        if not self.model_loaded:
            log.info(f"Loading Translation model: {settings.translation_model}")
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(settings.translation_model, trust_remote_code=True)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(settings.translation_model, trust_remote_code=True)
                if torch.cuda.is_available():
                    self.model = self.model.cuda()
                self.model_loaded = True
            except Exception as e:
                log.error(f"Translation load failed: {e}")
                raise

    async def translate(self, text: str, source_language: str, target_language: str = "english") -> str:
        if source_language.lower() == "english": return text
        try: self.load_model()
        except: return text

        try:
            src_code = self.lang_codes.get(source_language.lower())
            tgt_code = self.lang_codes.get(target_language.lower(), "eng_Latn")
            if not src_code: return text
            
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            if torch.cuda.is_available(): inputs = {k: v.cuda() for k, v in inputs.items()}
            
            with torch.no_grad():
                gen_tokens = self.model.generate(**inputs, forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(tgt_code), max_length=512)
            return self.tokenizer.batch_decode(gen_tokens, skip_special_tokens=True)[0].strip()
        except Exception as e:
            log.warning(f"Translation failed: {e}")
            return text

# Global Instances
audio_extractor = AudioExtractor()
transcription_service = TranscriptionService()
translation_service = TranslationService()
