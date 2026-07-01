# Farmer Outreach Report Generation Pipeline - Onboarding Guide

## 📌 Project Purpose

### The Problem We're Solving
We have launched an **agricultural outreach program** where we:
1. Visit farmers in rural areas
2. Demonstrate our AI-powered agri-chatbot
3. Provide them access to use the chatbot for agricultural guidance
4. Record audio of these interactions for documentation and analysis

**Challenge:** We have hundreds of audio recordings (in Punjabi/Hindi) that need to be converted into structured, professional reports for analysis, documentation, and decision-making.

**Solution:** An automated pipeline that takes raw audio recordings and generates comprehensive reports in multiple formats (PDF, Excel, Word).

---

## 🎯 What This Pipeline Does

**Input:** Audio/video recording of farmer interaction (Punjabi/Hindi)

**Output:** Professional reports containing:
- Meeting metadata (date, location, participants)
- Transcribed and translated conversation
- Key challenges identified
- Questions asked by farmers
- Crop disease terminology mapping
- AI-generated summary and conclusions

---

## 📊 Report Schema

### Report Structure

```
┌─────────────────────────────────────────────────────┐
│                  METADATA TABLE                      │
├──────────────────┬──────────────────────────────────┤
│ Date             │ 22-01-2026                       │
│ Day              │ Wednesday                        │
│ Village          │ Garhi Farid                      │
│ Name of Sarpanch │ Prakash Singh                    │
│ Panchayat        │ Gadi Blog Sri Chamkaur Sahib     │
│ Phone Number     │ 9876543210                       │
│ Block            │ Chamkaur Sahib                   │
│ Event Location   │ Community Center                 │
│ District         │ Rupnagar                         │
│ No of Farmers    │ 8                                │
│ Coordinator      │ Kshitij Kumar                    │
│ Female Farmers   │ 0                                │
│ Manager          │ Reporting Manager Name           │
│ Male Farmers     │ 8                                │
│ Event Start Time │ 10:00                            │
│ Event End Time   │ 12:00                            │
└──────────────────┴──────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                    NARRATION                         │
├─────────────────────────────────────────────────────┤
│ Summary:                                            │
│ On January 22nd, 2026, a farmer meeting was held   │
│ in village Gaddi Farid with 8 male farmers and     │
│ Sarpanch Prakash Singh, where participants         │
│ discussed their primary agricultural challenges... │
│                                                     │
│ Detailed Narration:                                │
│ Today's date is 22nd January 2026. The meeting    │
│ was held in village Gaddi Farid, Panchayat Gaddi  │
│ Block Sri Chamkaur Sahib, District Rupnagar...    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│        KEY CHALLENGES SHARED BY FARMERS             │
├─────────────────────────────────────────────────────┤
│ 1. Wild animal damage - Wild boars and nilgai     │
│    causing significant crop damage                 │
│ 2. Fertilizer quality concerns - Farmers reported  │
│    issues with fertilizer effectiveness            │
│ 3. Seed quality - Concerns about seed germination  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│           QUESTIONS ASKED BY FARMERS                │
├─────────────────────────────────────────────────────┤
│ 1. How to protect crops from wild animals?        │
│ 2. What is the recommended fertilizer dosage?     │
│ 3. How to use AI chatbot for disease detection?   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  CROP-WISE DISEASE TERMINOLOGY MAPPING              │
├──────┬─────────────┬──────────────┬────────────────┤
│ Crop │ Local Name  │ Standard     │ Scientific     │
│      │             │ Name         │ Name           │
├──────┼─────────────┼──────────────┼────────────────┤
│ Wheat│ Peeli Kungi │ Yellow Rust  │ Puccinia       │
│      │             │              │ striiformis    │
│ Wheat│ Gehun ka    │ Wheat Aphid  │ Sitobion       │
│      │ Keeda       │              │ avenae         │
└──────┴─────────────┴──────────────┴────────────────┘

┌─────────────────────────────────────────────────────┐
│              PARTICIPANTS DETAILS                    │
├────────┬────────────────────────────────────────────┤
│ SL No  │ Name                                       │
├────────┼────────────────────────────────────────────┤
│ 1      │ Prkaas Singh                               │
│ 2      │ Sireendr Singh                             │
│ 3      │ Kmjee Singh                                │
│ 4      │ Jsdeep Singh                               │
│ 5      │ Keern Deep Singh                           │
│ 6      │ Jgdeep Singh                               │
│ 7      │ Blvindr Singh                              │
└────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                   CONCLUSION                         │
├─────────────────────────────────────────────────────┤
│ This farmer interaction meeting served as a        │
│ crucial platform for addressing the multifaceted   │
│ agricultural challenges currently facing local     │
│ farming communities. The primary purpose was to... │
│                                                     │
│ [2-3 paragraphs of AI-generated conclusion]        │
└─────────────────────────────────────────────────────┘
```

---

## 🏗️ Current Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    DATA SOURCES                         │
├─────────────────────────────────────────────────────────┤
│  Zoho WorkDrive (Automated)  │  Local Files (Manual)    │
│  - Auto-sync folders         │  - Direct file upload    │
│  - Batch processing          │  - Custom metadata       │
└──────────────┬───────────────┴──────────────┬───────────┘
               │                              │
               └──────────────┬───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────┐
│                  PROCESSING PIPELINE                     │
└─────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
┌───────────────────────┐     ┌───────────────────────┐
│   1. AUDIO EXTRACTION │     │   2. TRANSCRIPTION    │
│   - FFmpeg            │────▶│   - Faster-Whisper    │
│   - Extract from video│     │   - GPU Accelerated   │
│   - Format conversion │     │   - Punjabi/Hindi     │
└───────────────────────┘     └───────────┬───────────┘
                                          │
                              ┌───────────▼───────────┐
                              │   3. TRANSLATION      │
                              │   - IndicTrans2       │
                              │   - GPU Accelerated   │
                              │   - Punjabi→English   │
                              └───────────┬───────────┘
                                          │
                              ┌───────────▼───────────┐
                              │   4. AI ANALYSIS      │
                              │   - Claude Sonnet 4.5 │
                              │   - Content extraction│
                              │   - Summarization     │
                              └───────────┬───────────┘
                                          │
                ┌─────────────────────────┼─────────────────────────┐
                ▼                         ▼                         ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│ 5. TRANSLITERATION    │ │ 6. PARTICIPANT PARSING│ │ 7. TERMINOLOGY MAPPING│
│ - Punjabi→English     │ │ - Name extraction     │ │ - Dialect→Scientific  │
│ - Smart capitalization│ │ - Categorization      │ │ - Crop disease mapping│
└───────────┬───────────┘ └───────────┬───────────┘ └───────────┬───────────┘
            │                         │                         │
            └─────────────────────────┼─────────────────────────┘
                                      ▼
                      ┌───────────────────────────┐
                      │   8. REPORT GENERATION    │
                      │   - PDF (ReportLab)       │
                      │   - Excel (OpenPyXL)      │
                      │   - Word (python-docx)    │
                      └───────────┬───────────────┘
                                  │
                      ┌───────────▼───────────┐
                      │   9. STORAGE          │
                      │   - MongoDB           │
                      │   - File System       │
                      └───────────────────────┘
```

---

## 🛠️ Technologies & Methods

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Audio Processing** | FFmpeg | Extract audio from video, format conversion |
| **Transcription** | Faster-Whisper (large-v3) | Speech-to-text for Punjabi/Hindi |
| **Translation** | IndicTrans2 | Punjabi/Hindi → English translation |
| **AI Analysis** | Claude Sonnet 4.5 (Anthropic) | Content extraction, summarization |
| **Database** | MongoDB | Store interaction records |
| **Report Generation** | ReportLab, OpenPyXL, python-docx | PDF, Excel, Word reports |
| **Cloud Storage** | Zoho WorkDrive API | Automated data ingestion |
| **GPU Acceleration** | CUDA (PyTorch) | Faster transcription & translation |

### Key Methods & Algorithms

#### 1. **Transliteration System**
```python
# Converts Punjabi Unicode → English ASCII
# Example: ਪਰਕਾਸ ਸਿੰਘ → Prkaas Singh

- Complete Gurmukhi character mapping (35+ consonants, 10+ vowels)
- Diacritical marks handling (ੰ, ਂ, ੱ)
- Smart capitalization for surnames (Singh, Kaur, Kumar)
```

#### 2. **Dual Extraction Strategy**
```python
# For mixed-format data
extract_parenthetical()  # "ਗੜੀ ਫਰੀਦ (Garhi Farid)" → "Garhi Farid"

# For pure Punjabi text
transliterate_punjabi_to_english()  # "ਪਰਕਾਸ ਸਿੰਘ" → "Prkaas Singh"
```

#### 3. **LLM Prompt Engineering**
```python
# Structured prompts for Claude to extract:
- Detailed narration
- Key challenges (numbered list)
- Farmer questions (numbered list)
- Terminology mapping (crop, local name, scientific name)
- Summary and conclusion
```

#### 4. **Batch Processing**
```python
# Merge multiple audio files → single report
- Download all files from Zoho folder
- Concatenate audio using FFmpeg
- Process as single interaction
```

---

## 📁 Project Structure

```
Outreach Dashboard/
├── src/
│   ├── main.py                 # CLI entry point
│   ├── pipeline.py             # Orchestrates entire workflow
│   ├── core/
│   │   ├── database.py         # MongoDB operations
│   │   ├── storage.py          # File management
│   │   └── utils.py            # Logging, validation
│   └── modules/
│       ├── processing.py       # Audio, transcription, translation
│       ├── analysis.py         # LLM analysis, transliteration
│       ├── reports.py          # PDF/Excel/Word generation
│       └── zoho.py             # Zoho WorkDrive integration
├── scripts/utils/
│   ├── inspect_record.py       # Database inspection
│   └── regenerate_report.py   # Report regeneration
├── data/
│   ├── audio/                  # Extracted audio files
│   ├── reports/                # Generated reports
│   └── temp/                   # Temporary files
├── config.py                   # Configuration
└── requirements.txt            # Dependencies
```

---

## ⚙️ Data Flow

### 1. **Automated Ingestion (Zoho)**
```bash
python -m src.main process-merge <FOLDER_ID> --village "Village Name"
```
- Downloads all files from Zoho folder
- Merges audio files
- Processes as single interaction
- Generates one comprehensive report

### 2. **Manual Processing (Local File)**
```bash
python -m src.main process-file audio.mp3 --village "Village" --district "District"
```
- Accepts local audio/video file
- Custom metadata via CLI arguments
- Processes single file
- Generates report

---

## 🚧 Current Problems & Limitations

### 1. **❗ CRITICAL: Speaker Identification Issue**
- **Issue:** Audio contains both facilitator questions (our team) AND farmer responses, but LLM cannot distinguish between speakers
- **Impact:** 
  - Facilitator questions incorrectly appear in "Questions Asked by Farmers" section
  - Facilitator prompts incorrectly appear in "Key Challenges Shared by Farmers" section
  - Report misrepresents who said what
- **Example:**
  - Facilitator asks: "Do you guys do soil testing?"
  - LLM extracts this as a farmer question ❌
- **Root Cause:** 
  - Transcription produces single text stream without speaker labels
  - LLM has no way to identify different voices
  - No speaker diarization in current pipeline
- **Status:** **HIGH PRIORITY** - Needs speaker diarization implementation
- **Proposed Solution:** 
  - Implement speaker diarization (pyannote.audio or similar)
  - Label speakers as "Facilitator" vs "Farmer"
  - Update LLM prompts to extract only farmer questions/challenges
  - Add "Facilitator Questions" as separate section if needed

### 2. **Transliteration Accuracy**
- **Issue:** Some Punjabi names don't transliterate perfectly (e.g., "Prkaas" instead of "Prakash")
- **Impact:** Names are readable but not phonetically perfect
- **Status:** Acceptable for current use, can be improved with better phonetic mapping

### 3. **LLM Dependency**
- **Issue:** Requires Anthropic API (paid service)
- **Impact:** Processing cost per interaction (~$0.10-0.50)
- **Status:** Acceptable for current volume, may need optimization for scale

### 4. **GPU Requirement**
- **Issue:** Faster-Whisper and IndicTrans2 are slow on CPU
- **Impact:** Processing time: ~15-20 min (GPU) vs 1-2 hours (CPU)
- **Status:** GPU recommended but not mandatory

### 5. **Manual Metadata Entry**
- **Issue:** For local files, metadata must be provided via CLI
- **Impact:** Requires manual input for each file
- **Status:** Acceptable for small batches, could be improved with GUI

### 6. **Zoho Token Expiry**
- **Issue:** Zoho refresh tokens expire periodically
- **Impact:** Requires manual token regeneration
- **Status:** Documented in README, needs periodic maintenance

---

## 🚀 Future Plans

### Phase 1: Immediate Improvements (1-2 months)
- [ ] **🔥 Speaker Diarization** - **CRITICAL PRIORITY**
  - Implement pyannote.audio or similar for speaker identification
  - Label speakers as "Facilitator" vs "Farmer" in transcription
  - Update LLM prompts to extract only farmer questions/challenges
  - Add separate "Facilitator Questions" section in report
  - Test accuracy with multi-speaker audio samples
- [ ] **Web Interface** - Build simple web UI for file upload and metadata entry
- [ ] **Batch Processing UI** - Allow multiple file uploads with CSV metadata
- [ ] **Report Templates** - Customizable report formats for different audiences
- [ ] **Email Notifications** - Auto-send reports when processing completes

### Phase 2: Enhanced Features (3-4 months)
- [ ] **Improved Transliteration** - Better phonetic mapping for Punjabi names
- [ ] **Multi-Language Support** - Add support for other regional languages (Tamil, Telugu, Bengali)
- [ ] **Audio Quality Enhancement** - Pre-processing to improve transcription accuracy
- [ ] **Advanced Speaker Features** - Speaker counting, speaker profiling, voice characteristics
- [ ] **Sentiment Analysis** - Detect farmer satisfaction levels per speaker

### Phase 3: Scale & Optimization (6+ months)
- [ ] **Cost Optimization** - Explore open-source LLM alternatives (Llama 3, Mistral)
- [ ] **Real-time Processing** - Live transcription during farmer interactions
- [ ] **Mobile App** - Record and process on mobile devices
- [ ] **Analytics Dashboard** - Aggregate insights across all interactions
- [ ] **Automated Insights** - Trend analysis, common challenges, regional patterns

### Phase 4: Advanced Features
- [ ] **Video Analysis** - Extract visual information (crop conditions, farmer expressions)
- [ ] **Knowledge Base Integration** - Link farmer questions to chatbot knowledge base
- [ ] **Recommendation Engine** - Suggest solutions based on historical data
- [ ] **Multi-modal Reports** - Include images, charts, and interactive elements

---

## 📚 Learning Resources

### For New Team Members

1. **Project Setup**
   - Read `README.md` for installation and usage
   - Review `scripts/README.md` for utility tools
   - Check `.env.example` for configuration

2. **Understanding the Code**
   - Start with `src/main.py` (CLI entry point)
   - Follow `src/pipeline.py` (main workflow)
   - Explore `src/modules/` (individual components)

3. **Testing**
   - Use `scripts/utils/inspect_record.py` to examine data
   - Test with small audio files first
   - Check `logs/pipeline.log` for debugging

4. **Key Concepts**
   - **Transliteration:** Punjabi Unicode → English ASCII
   - **LLM Prompting:** Structured extraction from Claude
   - **Batch Processing:** Merging multiple files
   - **Report Generation:** PDF layout with ReportLab

---

## 🤝 Contributing

### Development Workflow
1. Create feature branch
2. Make changes
3. Test with sample audio
4. Update documentation
5. Submit for review

### Code Standards
- Follow existing code structure
- Add comments for complex logic
- Update README if adding new features
- Test with real Punjabi audio

---

## 📞 Support

- **Documentation:** `README.md`, `scripts/README.md`
- **Logs:** `logs/pipeline.log`
- **Utilities:** `scripts/utils/`
- **Issues:** Check troubleshooting section in README

---

**Welcome to the team! 🎉**
