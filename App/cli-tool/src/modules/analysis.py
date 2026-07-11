"""
Content Analysis Module
Handles LLM-based analysis (Claude) and Participant Extraction
"""
from typing import Dict, List, Optional, Any
import json
from google import genai
from google.genai import types
from config import settings
from src.core.utils import log

def transliterate_punjabi_to_english(text: str) -> str:
    """Transliterate Punjabi/Hindi Unicode text to English/ASCII"""
    if not text:
        return text
    
    # Basic Gurmukhi/Devanagari to Latin transliteration mappings
    transliteration_map = {
        'ਅ': 'a', 'ਆ': 'aa', 'ਇ': 'i', 'ਈ': 'ee', 'ਉ': 'u', 'ਊ': 'oo', 'ਏ': 'e', 'ਐ': 'ai', 'ਓ': 'o', 'ਔ': 'au',
        'ਕ': 'k', 'ਖ': 'kh', 'ਗ': 'g', 'ਘ': 'gh', 'ਙ': 'ng',
        'ਚ': 'ch', 'ਛ': 'chh', 'ਜ': 'j', 'ਝ': 'jh', 'ਞ': 'ny',
        'ਟ': 't', 'ਠ': 'th', 'ਡ': 'd', 'ਢ': 'dh', 'ਣ': 'n',
        'ਤ': 't', 'ਥ': 'th', 'ਦ': 'd', 'ਧ': 'dh', 'ਨ': 'n',
        'ਪ': 'p', 'ਫ': 'ph', 'ਬ': 'b', 'ਭ': 'bh', 'ਮ': 'm',
        'ਯ': 'y', 'ਰ': 'r', 'ਲ': 'l', 'ਵ': 'v', 'ੜ': 'r',
        'ਸ': 's', 'ਹ': 'h', 'ਸ਼': 'sh', 'ਖ਼': 'kh', 'ਗ਼': 'gh', 'ਜ਼': 'z', 'ਫ਼': 'f',
        # Vowel signs (matras)
        'ਾ': 'aa', 'ਿ': 'i', 'ੀ': 'ee', 'ੁ': 'u', 'ੂ': 'oo', 'ੇ': 'e', 'ੈ': 'ai', 'ੋ': 'o', 'ੌ': 'au',
        # Important: Diacritical marks (nasalization)
        'ੰ': 'n',  # Bindi (tippi) - CRITICAL for "Singh"
        'ਂ': 'n',  # Bindi (Devanagari style)
        'ੱ': '',   # Addak (gemination)
        '੍': '',   # Halant (virama)
        # Hindi Devanagari
        'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng',
        'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'ny',
        'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
        'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
        'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
        'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh', 'ष': 'sh', 'स': 's', 'ह': 'h',
        'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee', 'उ': 'u', 'ऊ': 'oo', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
        'ा': 'aa', 'ि': 'i', 'ी': 'ee', 'ु': 'u', 'ू': 'oo', 'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', '्': '',
        'ं': 'n', 'ँ': 'n',  # Devanagari anusvara and chandrabindu
    }
    
    result = []
    for char in text:
        result.append(transliteration_map.get(char, char))
    
    transliterated = ''.join(result).strip()
    
    # Smart capitalization for names
    words = transliterated.split()
    capitalized_words = []
    for word in words:
        word_lower = word.lower()
        # Special cases for common surnames
        if word_lower == 'singh':
            capitalized_words.append('Singh')
        elif word_lower == 'kaur':
            capitalized_words.append('Kaur')
        elif word_lower == 'kumar':
            capitalized_words.append('Kumar')
        else:
            # Standard title case
            capitalized_words.append(word_lower.capitalize())
    
    return ' '.join(capitalized_words)


class ParticipantParser:
    """Parse and extract participant information"""
    
    @staticmethod
    async def parse_participants(metadata: Dict[str, Any], transcript: Optional[str] = None) -> Dict[str, Any]:
        log.info("Parsing participant information")
        participant_info = {
            "total_count": metadata.get("participant_count", 0),
            "farmer_names": metadata.get("farmer_names", []),
            "categories": metadata.get("farmer_categories", [])
        }
        
        # Extract from transcript using LLM if names missing
        if transcript and not participant_info["farmer_names"]:
            try:
                client = genai.Client(api_key=settings.gemini_api_key)
                prompt = f"""Analyze the following transcript of a rural village meeting and extract the names of all farmers or participants who spoke or were mentioned.
                
                Transcript:
                {transcript}
                
                Instructions:
                1. Identify specific individual names of farmers/participants.
                2. Exclude "Field Coordinator", "Farmer", "Speaker", or generic titles.
                3. Exclude the host/moderator names if possible.
                4. Return the result STRICTLY as a JSON array of strings. Example: ["Name1", "Name2"]
                5. If no specific names are mentioned, return an empty JSON array.
                6. Output ONLY the JSON string.
                
                JSON:"""
                
                response = client.models.generate_content(
                    model=settings.gemini_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=1024,
                        temperature=0.0
                    )
                )
                
                text = response.text.strip().replace('```json', '').replace('```', '')
                try:
                    names = json.loads(text)
                except:
                    names = [line.strip().lstrip('-•* ') for line in text.split('\n') if line.strip()]
                
                final_names = [n.strip() for n in names if isinstance(n, str) and n.strip() and len(n) < 40 and "transcript" not in n.lower()]
                
                if final_names:
                    participant_info["farmer_names"] = final_names
                    if participant_info["total_count"] < len(final_names):
                        participant_info["total_count"] = len(final_names)
                    log.info(f"LLM extracted {len(final_names)} names")
            except Exception as e:
                log.error(f"Failed to extract names: {e}")
                
        return participant_info

    @staticmethod
    def categorize_farmers(farmer_data: List[Dict[str, Any]]) -> List[str]:
        categories = []
        for f in farmer_data:
            size = f.get("land_size_acres", 0)
            if size == 0: categories.append("Landless farmer")
            elif size < 2.5: categories.append("Marginal farmer")
            elif size < 5: categories.append("Small farmer")
            elif size < 10: categories.append("Semi-medium farmer")
            elif size < 25: categories.append("Medium farmer")
            else: categories.append("Large farmer")
        return categories

class LLMAnalyzer:
    """Analyze transcripts using Gemini API"""
    
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
    
    async def analyze_full_interaction(self, transcript: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        log.info("Performing full interaction analysis")
        return {
            "narration": await self.generate_narration(transcript, metadata),
            "challenges": await self.extract_challenges(transcript),
            "questions": await self.extract_questions(transcript),
            "fallback_questions": [] # populated later if needed, optimized to avoid too many calls if not critical
        }
        # Note: Fallback questions were separated to reduce latency/cost if not explicitly needed, 
        # but can be re-added inside this dict if strictly required by report generator.
        # Adding them back to ensure parity with original behavior:
        res = await self._analyze_parallel(transcript, metadata)
        return res

    async def _analyze_parallel(self, transcript: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        # Helper to run sequential (or parallel) analysis
        narration = await self.generate_narration(transcript, metadata)
        challenges = await self.extract_challenges(transcript)
        questions = await self.extract_questions(transcript)
        fallback = await self.generate_fallback_questions(transcript, challenges)
        return {
            "narration": narration,
            "challenges": challenges, 
            "questions": questions, 
            "fallback_questions": fallback
        }

    async def generate_narration(self, transcript: str, metadata: Dict[str, Any]) -> Dict[str, str]:
        prompt = f"""You are a professional rapporteur.
        1. Create a "Cleaned Dictation" of this meeting transcript in English. It should look like a formal detailed narration of what happened, preserving the accuracy of the coordinator's or farmers' speech but removing filler words. It should be 2-3 detailed paragraphs.
        2. Create a "Summary" of the entire interaction in 1 small paragraph.
        
        Return STRICTLY valid JSON:
        {{
            "detailed_narration": "...",
            "summary": "..."
        }}

        Transcript: {transcript}"""
        
        response_text = await self._call_gemini(prompt)
        try:
            # Clean markdown code blocks
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            # Attempt to parse JSON
            start = clean_text.find('{')
            end = clean_text.rfind('}') + 1
            if start != -1 and end != -1:
                return json.loads(clean_text[start:end])
        except Exception as e:
            log.warning(f"JSON Parse failed: {e}")
            pass
            
        # Fallback if valid JSON fails
        return {
            "detailed_narration": response_text,
            "summary": "Summary generation failed."
        }

    async def extract_challenges(self, transcript: str) -> List[str]:
        prompt = f"""Analyze this transcript (which may be in Punjabi/Hindi) and extract key agricultural challenges mentioned by farmers.
        1. Output ONLY the challenges in English.
        2. Format as a numbered list.
        
        Transcript: {transcript}"""
        text = await self._call_gemini(prompt)
        return self._parse_list(text)

    async def extract_questions(self, transcript: str) -> List[str]:
        prompt = f"""Identify specific questions asked by farmers in this transcript.
        1. Classify each question as "Agricultural" or "Non-Agricultural".
        2. Discard Non-Agricultural questions.
        3. Discard general topics or statements. Only include actual queries/concerns requiring an answer.
        4. Rephrase Agricultural questions into clear, professional full sentences in English.
        
        Return them as a numbered list of ONLY the Agricultural questions.
        
        Transcript: {transcript}"""
        text = await self._call_gemini(prompt)
        return self._parse_list(text)

    async def extract_rich_metadata(self, transcript: str, current_meta: Dict[str, Any]) -> Dict[str, Any]:
        """Extract missing metadata fields from transcript"""
        prompt = f"""Extract the following details from the meeting transcript:
        - Sarpanch Name
        - Panchayat Name
        - Sarpanch Phone Number
        - Event Location
        - Event Start/End Time (approximate inferred)
        - Farmer Counts (Male/Female)
        
        Return JSON:
        {{
            "sarpanch_name": "...",
            "panchayat": "...",
            "sarpanch_phone": "...",
            "event_location": "...",
            "event_start_time": "...", 
            "event_end_time": "...",
            "farmer_counts": {{ "male": 0, "female": 0, "total": 0 }}
        }}
        
        Transcript: {transcript}"""
        
        try:
            res = await self._call_gemini(prompt)
            clean = res.replace("```json", "").replace("```", "").strip()
            start = clean.find('{')
            end = clean.rfind('}') + 1
            if start != -1:
                data = json.loads(clean[start:end])
                # Transliterate Punjabi fields to English
                if 'sarpanch_name' in data and data['sarpanch_name']:
                    data['sarpanch_name'] = transliterate_punjabi_to_english(data['sarpanch_name'])
                if 'panchayat' in data and data['panchayat']:
                    data['panchayat'] = transliterate_punjabi_to_english(data['panchayat'])
                if 'event_location' in data and data['event_location']:
                    data['event_location'] = transliterate_punjabi_to_english(data['event_location'])
                return {k: v for k, v in data.items() if v and str(v).lower() not in ["none", "null", "n/a", "unknown"]}
        except Exception as e:
            log.warning(f"Metadata extraction failed: {e}")
        return {}

    async def extract_terminology(self, transcript: str) -> List[Dict[str, str]]:
        """Extract agricultural terminology and map to scientific names"""
        prompt = f"""Analyze the transcript and identify specific local/dialect agricultural terms related to **Diseases**, **Pests**, or **Conditions** mentioned by farmers.
        
        For each term found:
        1. Identify the **Crop** (Wheat, Paddy, etc.)
        2. Identify the **Local/Dialect Name** (e.g., 'Peeli Kungi', 'Tela Chepa', 'Sheet Blight')
        3. Provide the **Standard/Common Name** in English (e.g., 'Yellow Rust', 'Aphid Infestation')
        4. Provide the **Scientific Name** (e.g., 'Puccinia striiformis', 'Sitobion avenae')
        5. Identify the **Language/Dialect** (e.g., 'Punjabi')
        
        Return a JSON ARRAY of objects:
        [
            {{
                "Crop": "Wheat",
                "Local Name": "ਪੀਲੀ ਕੁੰਗੀ (Peeli Kungi)",
                "Standard Name": "Yellow Rust",
                "Scientific Name": "Puccinia striiformis",
                "Language": "Punjabi"
            }}
        ]
        
        Reference Mappings (use these if found):
        - Peeli Kungi -> Yellow Rust -> Puccinia striiformis
        - Haldi Rog -> Yellowing Disease -> Physiological / Nutrient related
        - Tela Chepa -> Aphid Infestation -> Sitobion avenae / Rhopalosiphum padi
        - Sheet Blight -> Sheath Blight -> Rhizoctonia solani
        - Kala Tela -> Brown Planthopper -> Nilaparvata lugens
        - White Tela -> White-backed Planthopper -> Sogatella furcifera
        - Bona Rog -> Dwarfing -> Rice Dwarf
        
        Transcript: {transcript}"""
        
        try:
            res = await self._call_gemini(prompt)
            clean = res.replace("```json", "").replace("```", "").strip()
            start = clean.find('[')
            end = clean.rfind(']') + 1
            if start != -1:
                return json.loads(clean[start:end])
        except Exception as e:
            log.warning(f"Terminology extraction failed: {e}")
        return []

    async def generate_conclusion(self, transcript: str, narration: str, challenges: List[str], 
                                   questions: List[str], terminology: List[Dict[str, str]]) -> str:
        """Generate a comprehensive conclusion for the farmer interaction report"""
        # Prepare terminology summary
        term_summary = ""
        if terminology:
            term_summary = "\n\nDisease/Pest Issues Identified:\n"
            for t in terminology:
                term_summary += f"- {t.get('Crop', 'Unknown')}: {t.get('Local Name', '')} ({t.get('Standard Name', '')})\n"
        
        prompt = f"""Based on the following farmer interaction meeting details, write a comprehensive 2-3 paragraph conclusion summarizing:
1. The overall meeting purpose and outcomes
2. Key agricultural issues discussed
3. Actionable recommendations or next steps

Meeting Summary:
{narration}

Key Challenges:
{chr(10).join(f"- {c}" for c in challenges[:5])}

Farmer Questions:
{chr(10).join(f"- {q}" for q in questions[:5])}
{term_summary}

Write a professional, concise conclusion focusing on practical outcomes and recommendations. Use simple, clear language."""
        
        try:
            conclusion = await self._call_gemini(prompt, max_tokens=1024)
            return conclusion.strip()
        except Exception as e:
            log.error(f"Conclusion generation failed: {e}")
            return "Summary generation failed."


    async def _call_gemini(self, prompt: str, max_tokens: int = 2048) -> str:
        try:
            response = self.client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.3
                )
            )
            return response.text.strip()
        except Exception as e:
            log.error(f"LLM Call failed: {e}")
            return ""

    def _parse_list(self, text: str) -> List[str]:
        items = []
        for line in text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                item = line.lstrip('0123456789.-•) ').strip()
                if item: items.append(item)
        return items

participant_parser = ParticipantParser()
llm_analyzer = LLMAnalyzer()
