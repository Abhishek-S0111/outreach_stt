"""
Audio Processing Module
Handles Audio Extraction (FFmpeg), Transcription (Whisper), and Translation (IndicTrans2)
"""
from pathlib import Path
from typing import Optional, Dict, List, Any
import ffmpeg
import whisper
import torch
from faster_whisper import WhisperModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from config import settings
from src.core.utils import log

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

# --- Part 2: Transcription Service ---

class TranscriptionService:
    """Transcribe audio using Whisper"""
    
    def __init__(self):
        self.model = None
        self.model_loaded = False
        
    def load_model(self):
        if not self.model_loaded:
            log.info(f"Loading Whisper model: {settings.whisper_model}")
            try:
                self.model = WhisperModel(
                    settings.whisper_model,
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
