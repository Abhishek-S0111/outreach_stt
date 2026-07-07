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
import numpy as np
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook

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


# --- Part 1.5: Audio Preprocessing ---

class AudioPreProcessing:
    """Pre-process audio files: noise suppression and speaker diarization"""
    
    def __init__(self):
        self.diarization_pipeline = None
        self.diarization_loaded = False

    @staticmethod
    def load_audio(audio_path: Path) -> List[Any]:
        """Load audio file using librosa"""
        if not audio_path.exists():
            raise FileNotFoundError(f"Invalid Audio Path: {audio_path}")
        
        try:
            y, sr = librosa.load(audio_path, sr=None)
            return [y, sr]
        except Exception as e:
            log.error(f"Error loading audio file: {e}")
            raise

    @staticmethod
    def noise_suppression(audio_path: Path, output_path: Optional[Path] = None) -> Path:
        """Apply non-stationary noise reduction to audio file"""
        log.info(f"Applying noise suppression to {audio_path.name}")
        aud = AudioPreProcessing.load_audio(audio_path)
        y = aud[0]
        sr = aud[1]

        try:
            y_denoised = nr.reduce_noise(y=y, sr=sr, stationary=False, prop_decrease=0.85)
        except Exception as e:
            log.error(f"Noise reduction failed: {e}")
            raise

        target_path = output_path or audio_path
        sf.write(target_path, y_denoised, sr)
        log.info(f"Noise suppression complete. Saved to: {target_path}")
        return target_path

    # Keep compatibility with original method spelling
    @staticmethod
    def noise_suppresion(audio_path: Path, output_path: Optional[Path] = None) -> Path:
        return AudioPreProcessing.noise_suppression(audio_path, output_path)

    def load_diarization_model(self, hf_token: Optional[str] = None):
        """Lazy load Pyannote Speaker Diarization Pipeline"""
        if not self.diarization_loaded:
            token = hf_token or getattr(settings, "hf_token", None) or os.getenv("HF_TOKEN")
            if not token:
                log.warning("Hugging Face Access Token (HF_TOKEN) is not configured. Pyannote model download/auth may fail.")
            
            model_name = getattr(settings, "diarization_model", "pyannote/speaker-diarization-community-1")
            log.info(f"Initializing Pyannote Speaker Diarization Pipeline ({model_name})...")
            
            try:
                self.diarization_pipeline = Pipeline.from_pretrained(
                    model_name,
                    token=token
                )
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                self.diarization_pipeline.to(device)
                self.diarization_loaded = True
                log.info(f"Diarization pipeline loaded successfully on {device}.")
            except Exception as e:
                log.error(f"Failed to load Pyannote pipeline: {e}")
                raise

    async def diarize(
        self,
        audio_path: Path,
        hf_token: Optional[str] = None,
        num_speakers: int = 0,
        min_speakers: int = 0,
        max_speakers: int = 0,
        output_json_path: Optional[Path] = None
    ) -> List[Dict[str, Any]]:
        """
        Run speaker diarization on audio file.
        Returns a list of segments with start time, end time, and speaker label.
        Optionally saves segments to output_json_path.
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        self.load_diarization_model(hf_token=hf_token)
        
        log.info(f"Running Speaker Diarization on {audio_path.name}")
        
        # Setup pipeline params
        diarization_params = {}
        if num_speakers > 0:
            diarization_params["num_speakers"] = num_speakers
        else:
            if min_speakers > 0:
                diarization_params["min_speakers"] = min_speakers
            if max_speakers > 0:
                diarization_params["max_speakers"] = max_speakers

        try:
            with ProgressHook() as hook:
                diarization_output = self.diarization_pipeline(str(audio_path), hook=hook, **diarization_params)

            # Extract speaker segments
            raw_speaker_segments = []
            for turn, speaker in diarization_output.speaker_diarization:
                raw_speaker_segments.append({
                    "start": turn.start,
                    "end": turn.end,
                    "speaker": speaker
                })

            log.info(f"Diarization complete. Identified {len(set(s['speaker'] for s in raw_speaker_segments))} unique speaker(s).")

            # Save raw segments to JSON file if path is provided
            if output_json_path:
                output_json_path = Path(output_json_path)
                output_json_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_json_path, "w", encoding="utf-8") as f:
                    json.dump(raw_speaker_segments, f, indent=4, ensure_ascii=False)
                log.info(f"Raw speaker timeline exported to: '{output_json_path}'")

            return raw_speaker_segments

        except Exception as e:
            log.error(f"Diarization failed: {e}")
            raise


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
audio_preprocessing = AudioPreProcessing()
transcription_service = TranscriptionService()
translation_service = TranslationService()
