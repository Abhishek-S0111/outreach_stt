"""
Report Generation Module
Handles creation of Excel, PDF, and Word reports
"""
import re
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from docx import Document
from docx.shared import RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from src.core.utils import log
from src.modules.analysis import transliterate_punjabi_to_english

def extract_parenthetical(text: str) -> str:
    """Extract ONLY content in parentheses, else extract English only"""
    if not text:
        return text
    
    text = str(text)
    # First try to extract content in parentheses
    import re
    paren_match = re.search(r'\(([^)]+)\)', text)
    if paren_match:
        result = paren_match.group(1).strip()
        # Capitalize first letter of each word
        return result.title()
    
    # If no parentheses, extract ASCII only
    result = []
    for char in text:
        if ord(char) < 128:  # ASCII range
            result.append(char)
    
    cleaned = ''.join(result).strip()
    # Remove multiple spaces
    while '  ' in cleaned:
        cleaned = cleaned.replace('  ', ' ')
    
    # Capitalize
    return cleaned.title() if cleaned else text

def strip_markdown(text: str) -> str:
    """Remove markdown formatting symbols from text"""
    if not text:
        return text
    # Remove markdown headers (##, ###, etc.)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Remove bold/italic markers (**text** or *text*)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **text**
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *text*
    text = text.replace('__', '').replace('_', '')
    return text.strip()

class ExcelReportGenerator:
    """Generate Excel reports"""
    @staticmethod
    def create_report(data: Dict[str, Any], output_path: Path) -> Path:
        log.info("Generating Excel report")
        wb = Workbook()
        ws_summary = wb.active; ws_summary.title = "Summary"
        ExcelReportGenerator._create_summary_sheet(ws_summary, data)
        ExcelReportGenerator._create_details_sheet(wb.create_sheet("Details"), data)
        ExcelReportGenerator._create_participants_sheet(wb.create_sheet("Participants"), data)
        wb.save(output_path)
        log.info(f"Excel report saved: {output_path}")
        return output_path

    @staticmethod
    def _create_summary_sheet(ws, data: Dict[str, Any]):
        ws['A1'] = "Farmer Interaction Report"; ws['A1'].font = Font(size=16, bold=True, color="FFFFFF")
        ws['A1'].fill = PatternFill(start_color="2E75B6", end_color="2E75B6", fill_type="solid")
        ws.merge_cells('A1:D1')
        metadata = data.get('metadata', {})
        fields = [
            ("Date:", metadata.get('date', 'N/A')), ("Time:", metadata.get('time', 'N/A')),
            ("Location:", f"{metadata.get('village', '')}, {metadata.get('block', '')}, {metadata.get('district', '')}"),
            ("Coordinator:", metadata.get('coordinator_name', 'N/A')),
            ("Interaction Type:", metadata.get('interaction_type', 'N/A'))
        ]
        row = 3
        for label, value in fields:
            ws[f'A{row}'] = label; ws[f'A{row}'].font = Font(bold=True)
            ws[f'B{row}'] = str(value); row += 1
        
        row += 1; ws[f'A{row}'] = "Statistics"; ws[f'A{row}'].font = Font(size=14, bold=True); row += 1
        ws[f'A{row}'] = "Total Participants:"; ws[f'B{row}'] = data.get('participants', {}).get('total_count', 0); row += 1
        ws[f'A{row}'] = "Challenges:"; ws[f'B{row}'] = len(data.get('key_challenges', [])); row += 1
        ws[f'A{row}'] = "Questions:"; ws[f'B{row}'] = len(data.get('farmer_questions', []))
        ws.column_dimensions['A'].width = 25; ws.column_dimensions['B'].width = 50

    @staticmethod
    def _create_details_sheet(ws, data: Dict[str, Any]):
        ws['A1'] = "Interaction Details"; ws['A1'].font = Font(size=14, bold=True)
        row = 3; ws[f'A{row}'] = "Detailed Narration:"; ws[f'A{row}'].font = Font(size=12, bold=True); row += 1
        
        # Handle new Dict narration
        raw_narration = data.get('narration', 'N/A')
        if isinstance(raw_narration, dict):
            narration_text = f"Summary:\n{raw_narration.get('summary', '')}\n\nDetailed Translation:\n{raw_narration.get('detailed_narration', '')}"
        else:
            narration_text = str(raw_narration)
            if data.get('interaction_summary'):
                narration_text = f"Summary:\n{data.get('interaction_summary', '')}\n\nDetailed:\n{narration_text}"

        ws[f'A{row}'] = narration_text; ws[f'A{row}'].alignment = Alignment(wrap_text=True, vertical='top')
        ws.merge_cells(f'A{row}:D{row}'); row += 3
        
        for title, key in [("Key Challenges", 'key_challenges'), ("Questions", 'farmer_questions')]:
            ws[f'A{row}'] = title; ws[f'A{row}'].font = Font(size=12, bold=True); row += 1
            for i, item in enumerate(data.get(key, []), 1):
                ws[f'A{row}'] = f"{i}."; ws[f'B{row}'] = item; ws[f'B{row}'].alignment = Alignment(wrap_text=True)
                ws.merge_cells(f'B{row}:D{row}'); row += 1
            row += 1
        ws.column_dimensions['B'].width = 80

    @staticmethod
    def _create_participants_sheet(ws, data: Dict[str, Any]):
        ws['A1'] = "Participant Details"; ws['A1'].font = Font(size=14, bold=True)
        participants = data.get('participants', {})
        row = 3; ws[f'A{row}'] = "Total:"; ws[f'B{row}'] = participants.get('total_count', 0); row += 2
        
        names = participants.get('farmer_names', [])
        if names:
            ws[f'A{row}'] = "Names:"; ws[f'A{row}'].font = Font(bold=True); row += 1
            for i, name in enumerate(names, 1):
                ws[f'A{row}'] = f"{i}."; ws[f'B{row}'] = name; row += 1
        ws.column_dimensions['A'].width = 25; ws.column_dimensions['B'].width = 40

class PDFReportGenerator:
    """Generate PDF reports"""
    def __init__(self):
        try:
            pdfmetrics.registerFont(TTFont('FreeSans', Path("assets/fonts/FreeSans.ttf")))
            self.font = 'FreeSans'; self.header_font = 'Helvetica-Bold'
        except:
            self.font = 'Helvetica'; self.header_font = 'Helvetica-Bold'

    def create_report(self, data: Dict[str, Any], output_path: Path) -> Path:
        log.info("Generating PDF report")
        doc = SimpleDocTemplate(str(output_path), pagesize=A4, 
                              leftMargin=0.5*inch, rightMargin=0.5*inch, 
                              topMargin=0.5*inch, bottomMargin=0.5*inch)
        styles = getSampleStyleSheet()
        body_style = ParagraphStyle('Body', parent=styles['BodyText'], fontName=self.font, leading=14, fontSize=10)
        
        story = [
            Paragraph("Project Ajrasakha - Farmers outreach Project", styles['Title']),
            # Subtitle removed
            Spacer(1, 0.2*inch)
        ]
        
        # --- Metadata Table (2-Column Format) ---
        meta = data.get('metadata', {})
        parts = data.get('participants', {})
        farmer_counts = meta.get('farmer_counts', {})
        
        date_obj = meta.get('date')
        day_str = date_obj.strftime("%A") if isinstance(date_obj, datetime) else "N/A"
        date_str = date_obj.strftime("%d-%m-%Y") if isinstance(date_obj, datetime) else str(date_obj)
        
        # Extract ONLY parenthetical content from metadata fields, handle None
        village = extract_parenthetical(meta.get('village') or '')
        sarpanch = extract_parenthetical(meta.get('sarpanch_name') or '')
        panchayat = extract_parenthetical(meta.get('panchayat') or '')
        location = extract_parenthetical(meta.get('event_location') or '')
        block = extract_parenthetical(meta.get('block') or '')
        district = extract_parenthetical(meta.get('district') or '')
        coordinator = extract_parenthetical(meta.get('coordinator_name') or '')
        manager = extract_parenthetical(meta.get('reporting_manager_name') or '')

        table_data = [
            ['Date', date_str, 'Day', day_str],
            ['Village', village, 'Name of the Sarpanch', sarpanch],
            ['Panchayat', panchayat, 'Phone Number', meta.get('sarpanch_phone', '')],
            ['Block', block, 'Event Location', location],
            ['District', district, 'No of Farmers attended', parts.get('total_count', 0)],
            ['Name of the Coordinator', coordinator, 'Female Farmers', farmer_counts.get('female', '')],
            ['Name of the Reporting Manager', manager, 'Male Farmers', farmer_counts.get('male', '')],
            ['Event Start Time', meta.get('event_start_time', '10:00'), 'Event End Time', meta.get('event_end_time', '12:00')]
        ]
        
        # Widen first column to prevent "Name of the Reporting Manager" overflow
        col_widths = [2.0*inch, 1.8*inch, 1.8*inch, 2.0*inch]
        
        tbl = Table(table_data, colWidths=col_widths, style=TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTNAME', (0,0), (-1,-1), self.font),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('BACKGROUND', (0,0), (0,-1), colors.whitesmoke),
            ('BACKGROUND', (2,0), (2,-1), colors.whitesmoke),
            ('FONTNAME', (0,0), (0,-1), self.header_font),
            ('FONTNAME', (2,0), (2,-1), self.header_font),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 4),
            ('WORD_WRAP', (0,0), (-1,-1), True),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 0.2*inch))
        
        # --- Detailed Narration ---
        story.append(Table([['Detailed Narration of the Interaction:']], colWidths=[7.3*inch], style=TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
            ('FONTNAME', (0,0), (-1,-1), self.header_font),
            ('FONTSIZE', (0,0), (-1,-1), 10),
        ])))
        
        raw_narration = data.get('narration', {})
        if isinstance(raw_narration, dict):
            detailed_text = raw_narration.get('detailed_narration', '')
            summary_text = raw_narration.get('summary', '')
            # Keep summary even if it says "failed" - it's still content
        else:
            detailed_text = str(raw_narration)
            summary_text = data.get('interaction_summary', '')

        narration_content = []
        if detailed_text:
            narration_content.append(Paragraph("<b>Translation / Dictation:</b>", body_style))
            dt = detailed_text if detailed_text else ""
            narration_content.append(Paragraph(dt.replace('\\n', '<br/>'), body_style))
            narration_content.append(Spacer(1, 0.1*inch))
            
        if summary_text:
            narration_content.append(Paragraph("<b>Summary:</b>", body_style))
            narration_content.append(Paragraph(summary_text, body_style))

        story.append(Table([[narration_content]], colWidths=[7.3*inch], style=TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 6),
        ])))
        story.append(Spacer(1, 0.2*inch))
        
        # --- Key Challenges (Boxed) ---
        challenges = data.get('key_challenges', [])
        if challenges:
            story.append(Table([['Key Challenges Shared by the farmers']], colWidths=[7.3*inch], style=TableStyle([
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
                ('FONTNAME', (0,0), (-1,-1), self.header_font),
                ('FONTSIZE', (0,0), (-1,-1), 10),
            ])))
            
            challenges_text = []
            for i, chal in enumerate(challenges, 1):
                # Strip markdown from challenges
                clean_chal = strip_markdown(str(chal))
                challenges_text.append(Paragraph(f"{i}. {clean_chal}", body_style))
                challenges_text.append(Spacer(1, 6))
            
            story.append(Table([[challenges_text]], colWidths=[7.3*inch], style=TableStyle([
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('PADDING', (0,0), (-1,-1), 6),
            ])))
            story.append(Spacer(1, 0.2*inch))

        # --- Questions (Boxed) ---
        questions = data.get('farmer_questions', [])
        if questions:
            story.append(Table([['Questions asked by farmers']], colWidths=[7.3*inch], style=TableStyle([
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
                ('FONTNAME', (0,0), (-1,-1), self.header_font),
                ('FONTSIZE', (0,0), (-1,-1), 10),
            ])))
            
            q_content = []
            for i, q in enumerate(questions, 1):
                q_content.append(Paragraph(f"{i}. {q}", body_style))
                
            story.append(Table([[q_content]], colWidths=[7.3*inch], style=TableStyle([
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('PADDING', (0,0), (-1,-1), 6),
            ])))
            story.append(Spacer(1, 0.2*inch))

        # --- Terminology Mapping Table ---
        terms = data.get('terminology_mapping', [])
        if terms:
            story.append(Paragraph("Crop-wise Disease Terminology Mapping (Dialect to Scientific)", styles['Heading2']))
            story.append(Spacer(1, 6))
            
            term_data = [['Crop', 'Local / Dialect Name', 'Standard / Common Name', 'Scientific Name', 'Language / Dialect']]
            for t in terms:
                # Extract only English from Local Name (remove Punjabi Unicode)
                local_name = extract_parenthetical(t.get('Local Name', '-'))
                term_data.append([
                    t.get('Crop', '-'),
                    local_name if local_name else '-',
                    t.get('Standard Name', '-'),
                    t.get('Scientific Name', '-'),
                    t.get('Language', '-')
                ])
            
            # Optimized widths with better distribution
            term_widths = [0.9*inch, 1.2*inch, 2.0*inch, 2.2*inch, 1.0*inch]
            
            term_tbl = Table(term_data, colWidths=term_widths, style=TableStyle([
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('FONTNAME', (0,0), (-1,0), self.header_font),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('WORDWRAP', (0,0), (-1,-1), True),  # Enable word wrapping
            ]))
            story.append(term_tbl)
            story.append(Spacer(1, 0.2*inch))

        # --- Participants Details (Simplified) ---
        story.append(Paragraph("Participants Details", styles['Heading2']))
        story.append(Spacer(1, 6))
        
        p_headers = ['SL No', 'Name']
        p_data = [p_headers]
        
        farmer_names = parts.get('farmer_names', [])
        count = 0
        for name in farmer_names:
            count += 1
            # Use TRANSLITERATION for pure Punjabi names (now with smart capitalization)
            safe_name = transliterate_punjabi_to_english(str(name)) if name else ""
            p_data.append([str(count), safe_name])
            
        # Fill remaining rows up to 7 (not 8, to avoid empty last row)
        while count < 7:
            count += 1
            p_data.append([str(count), ""])

        p_widths = [0.6*inch, 6.7*inch]  # Two columns only
        
        p_tbl = Table(p_data, colWidths=p_widths, style=TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTNAME', (0,0), (-1,0), self.header_font),
            ('ALIGN', (0,0), (0,-1), 'CENTER'),  # Center SL No
            ('ALIGN', (1,0), (1,-1), 'LEFT'),    # Left-align names
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
        ]))
        story.append(p_tbl)
        story.append(Spacer(1, 0.2*inch))
        
        # --- Conclusion Section ---
        conclusion = data.get('conclusion', '')
        if conclusion and 'failed' not in conclusion.lower():
            # Strip markdown formatting
            conclusion_clean = strip_markdown(conclusion)
            
            story.append(Table([['Conclusion']], colWidths=[7.3*inch], style=TableStyle([
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
                ('FONTNAME', (0,0), (-1,-1), self.header_font),
                ('FONTSIZE', (0,0), (-1,-1), 10),
            ])))
            
            conclusion_content = [Paragraph(conclusion_clean, body_style)]
            
            story.append(Table([[conclusion_content]], colWidths=[7.3*inch], style=TableStyle([
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('PADDING', (0,0), (-1,-1), 6),
            ])))

        doc.build(story)
        log.info(f"PDF report saved: {output_path}")
        return output_path

class WordReportGenerator:
    """Generate Word reports"""
    @staticmethod
    def create_report(data: Dict[str, Any], output_path: Path) -> Path:
        log.info("Generating Word report")
        doc = Document()
        doc.add_heading('Farmer Interaction Report', 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Metadata
        meta = data.get('metadata', {})
        table = doc.add_table(rows=1, cols=2)
        for label, val in [("Date", meta.get('date')), ("Village", meta.get('village')), ("Coordinator", meta.get('coordinator_name'))]:
            row = table.add_row().cells
            row[0].text = label; row[1].text = str(val)
            
        # Content
        doc.add_heading('Narration', 1)
        doc.add_paragraph(data.get('narration', ''))
        
        for title, key in [("Challenges", 'key_challenges'), ("Questions", 'farmer_questions')]:
            doc.add_heading(title, 1)
            for i, item in enumerate(data.get(key, []), 1):
                doc.add_paragraph(f"{i}. {item}")
        
        doc.save(output_path)
        log.info(f"Word report saved: {output_path}")
        return output_path

excel_generator = ExcelReportGenerator()
pdf_generator = PDFReportGenerator()
word_generator = WordReportGenerator()
