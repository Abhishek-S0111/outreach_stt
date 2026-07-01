#!/usr/bin/env python3
"""
Fix the summary issue and regenerate report
"""
import asyncio
from src.core.database import DatabaseManager
from src.modules.reports import pdf_generator
from src.modules.analysis import LLMAnalyzer
from config import settings

# API key loaded from .env via settings
# settings.anthropic_api_key is automatically loaded from environment

IID = "6979fbb468f18e06ffe46303"

async def main():
    db = DatabaseManager()
    await db.connect()
    
    # Get record
    rec = await db.get_interaction_raw(IID)
    print(f"=== Processing: {rec['original_filename']} ===")
    
    # Check current summary
    narr = rec.get('narration', {})
    if isinstance(narr, dict):
        current_summary = narr.get('summary', '')
        detailed = narr.get('detailed_narration', '')
        print(f"Current summary: {current_summary[:100]}...")
        
        # If summary failed, regenerate it
        if 'failed' in current_summary.lower():
            print("\n=== Regenerating Summary ===")
            llm = LLMAnalyzer()
            
            # Generate new summary from detailed narration
            prompt = f"""Summarize the following detailed farmer meeting narration into 2-3 concise sentences:

{detailed[:3000]}

Provide a brief, professional summary focusing on key topics and outcomes."""
            
            try:
                new_summary = await llm._call_claude(prompt, max_tokens=512)
                print(f"Generated new summary ({len(new_summary)} chars):")
                print(new_summary)
                
                # Update narration dict
                narr['summary'] = new_summary
                await db.update_interaction(IID, {'narration': narr})
                print("\n✓ Summary updated in database")
            except Exception as e:
                print(f"Failed to generate summary: {e}")
    
    # Regenerate conclusion as well
    print("\n=== Regenerating Conclusion ===")
    llm = LLMAnalyzer()
    
    transcript = rec.get('transcript', '')
    challenges = rec.get('key_challenges', [])
    questions = rec.get('farmer_questions', [])
    terminology = rec.get('terminology_mapping', [])
    
    narration_text = narr.get('summary', '') or narr.get('detailed_narration', '') if isinstance(narr, dict) else str(narr)
    
    conclusion = await llm.generate_conclusion(
        transcript=transcript,
        narration=narration_text,
        challenges=challenges,
        questions=questions,
        terminology=terminology
    )
    
    print(f"Generated conclusion ({len(conclusion)} chars)")
    await db.update_interaction(IID, {'conclusion': conclusion})
    
    # Generate PDF
    print("\n=== Generating PDF Report ===")
    rec_updated = await db.get_interaction_raw(IID)
    
    from pathlib import Path
    report_dir = Path(f"data/reports/{IID}")
    report_dir.mkdir(parents=True, exist_ok=True)
    output_path = report_dir / "report_pdf_FINAL.pdf"
    
    report_data = {
        'metadata': rec_updated.get('metadata', {}),
        'participants': rec_updated.get('participants', {}),
        'narration': rec_updated.get('narration', {}),
        'key_challenges': rec_updated.get('key_challenges', []),
        'farmer_questions': rec_updated.get('farmer_questions', []),
        'terminology_mapping': rec_updated.get('terminology_mapping', []),
        'conclusion': rec_updated.get('conclusion', '')
    }
    
    pdf_generator.create_report(report_data, output_path)
    print(f"✓ Generated PDF: {output_path}")
    
    await db.disconnect()
    print("\n✅ COMPLETE")

if __name__ == "__main__":
    asyncio.run(main())
