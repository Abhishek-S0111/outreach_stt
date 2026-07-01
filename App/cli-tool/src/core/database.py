"""
Database and Storage Management
Combines MongoDB operations, Data Models, and File Management
"""
from typing import Optional, List, Dict, Any, Annotated, Union
from datetime import datetime
from pathlib import Path
import hashlib
import shutil
import aiofiles
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import BaseModel, Field, BeforeValidator
from bson import ObjectId
from config import settings
from src.core.utils import log

# --- Part 1: Models ---

# Utility function for validation
def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

# Pydantic v2 compatible ObjectId type
PyObjectId = Annotated[str, BeforeValidator(str)]

class InteractionMetadata(BaseModel):
    """Metadata for farmer interaction"""
    date: datetime
    time: str
    location: Optional[Dict[str, float]] = None
    village: str
    block: str
    district: str
    state: str = "Punjab"
    coordinator_name: str
    reporting_manager_name: Optional[str] = None
    interaction_type: str
    language: str = "punjabi"
    source_folder_path: Optional[str] = None
    
    # New fields for detailed report
    panchayat: Optional[str] = None
    sarpanch_name: Optional[str] = None
    sarpanch_phone: Optional[str] = None
    event_location: Optional[str] = None
    event_start_time: Optional[str] = None
    event_end_time: Optional[str] = None
    farmer_counts: Optional[Dict[str, int]] = None  # keys: male, female, total

class ParticipantInfo(BaseModel):
    """Information about interaction participants"""
    total_count: int
    farmer_names: List[str] = []
    categories: List[str] = []

class ProcessingStatus(BaseModel):
    """Track processing status of each stage"""
    audio_extracted: bool = False
    transcribed: bool = False
    translated: bool = False
    analyzed: bool = False
    report_generated: bool = False
    error: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class InteractionRecord(BaseModel):
    """Main interaction record stored in MongoDB"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    
    # File information
    original_filename: str
    file_path: str
    file_type: str
    file_size_mb: float
    
    # Metadata
    metadata: InteractionMetadata
    
    # Processing results
    audio_path: Optional[str] = None
    transcript: Optional[str] = None
    transcript_language: Optional[str] = None
    translation: Optional[str] = None
    
    # Analysis results (can be string or dict with detailed_narration/summary)
    narration: Optional[Union[str, Dict[str, str]]] = None  # Now strictly the CLEANED TRANSLATION
    interaction_summary: Optional[str] = None  # New field for the LLM SUMMARY
    key_challenges: List[str] = []
    farmer_questions: List[str] = []
    llm_fallback_questions: List[str] = []
    
    # Terminology Mapping
    terminology_mapping: List[Dict[str, str]] = []
    
    # Conclusion
    conclusion: Optional[str] = None
    
    # Participant information
    
    # Participant information
    participants: Optional[ParticipantInfo] = None
    
    # Photos
    photo_paths: List[str] = []
    
    # Generated reports
    excel_report_path: Optional[str] = None
    pdf_report_path: Optional[str] = None
    word_report_path: Optional[str] = None
    
    # Processing status
    status: ProcessingStatus = Field(default_factory=ProcessingStatus)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ReportTemplate(BaseModel):
    """Report template configuration"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    description: Optional[str] = None
    template_type: str
    config: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# --- Part 2: Database Manager ---

class DatabaseManager:
    """Manage MongoDB connections and operations"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
    
    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.mongodb_uri)
            self.db = self.client[settings.mongodb_database]
            await self.client.admin.command('ping')
            log.info(f"Connected to MongoDB: {settings.mongodb_database}")
            await self._create_indexes()
        except Exception as e:
            log.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def disconnect(self):
        if self.client:
            self.client.close()
            log.info("Disconnected from MongoDB")
    
    async def _create_indexes(self):
        await self.db.interactions.create_index("created_at")
        await self.db.interactions.create_index("metadata.date")
        await self.db.interactions.create_index("metadata.village")
        
    async def create_interaction(self, interaction: InteractionRecord) -> str:
        result = await self.db.interactions.insert_one(
            interaction.model_dump(by_alias=True, exclude={"id"})
        )
        return str(result.inserted_id)
    
    async def get_interaction(self, interaction_id: str) -> Optional[InteractionRecord]:
        doc = await self.db.interactions.find_one({"_id": ObjectId(interaction_id)})
        return InteractionRecord(**doc) if doc else None
    
    async def get_interaction_raw(self, interaction_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve interaction as raw dict (bypass Pydantic validation)"""
        return await self.db.interactions.find_one({"_id": ObjectId(interaction_id)})
    
    async def update_interaction(self, interaction_id: str, update_data: Dict[str, Any]) -> bool:
        update_data["updated_at"] = datetime.utcnow()
        result = await self.db.interactions.update_one(
            {"_id": ObjectId(interaction_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    async def list_interactions(self, skip: int = 0, limit: int = 50, filters: Optional[Dict[str, Any]] = None) -> List[InteractionRecord]:
        cursor = self.db.interactions.find(filters or {}).skip(skip).limit(limit).sort("created_at", -1)
        return [InteractionRecord(**doc) async for doc in cursor]

# --- Part 3: File Manager ---

class FileManager:
    """Manage file storage operations"""
    
    @staticmethod
    def get_file_size_mb(file_path: Path) -> float:
        return round(file_path.stat().st_size / (1024 * 1024), 2)

    @staticmethod
    def generate_unique_filename(original_filename: str, prefix: str = "") -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        file_hash = hashlib.md5(f"{original_filename}{timestamp}".encode()).hexdigest()[:8]
        file_path = Path(original_filename)
        return f"{prefix + '_' if prefix else ''}{timestamp}_{file_hash}_{file_path.name}"

    @staticmethod
    async def save_processed_file(source_path: Path, filename: str, subdir: str = "") -> Path:
        save_dir = settings.upload_dir / subdir if subdir else settings.upload_dir
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = save_dir / filename
        shutil.copy2(source_path, save_path)
        return save_path

    @staticmethod
    async def save_upload(file_content: bytes, filename: str, subdir: str = "") -> Path:
        unique_filename = FileManager.generate_unique_filename(filename, "upload")
        save_dir = settings.upload_dir / subdir if subdir else settings.upload_dir
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = save_dir / unique_filename
        
        async with aiofiles.open(save_path, 'wb') as f:
            await f.write(file_content)
        return save_path

    @staticmethod
    async def save_report(source_path: Path, report_type: str, interaction_id: str) -> Path:
        report_dir = settings.reports_dir / interaction_id
        report_dir.mkdir(parents=True, exist_ok=True)
        filename = f"report_{report_type}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}{source_path.suffix}"
        save_path = report_dir / filename
        shutil.copy2(source_path, save_path)
        return save_path

# Global instances
db_manager = DatabaseManager()
file_manager = FileManager()
