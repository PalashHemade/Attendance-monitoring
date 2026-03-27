import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_defaulter_letters(defaulters: list) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    normal_style.fontSize = 11
    normal_style.leading = 14
    
    bold_style = ParagraphStyle(
        'BoldStyle',
        parent=styles["Normal"],
        fontSize=11,
        fontName='Helvetica-Bold',
        leading=14
    )

    story = []
    
    for student in defaulters:
        student_name = student.get("name", "Unknown")
        student_prn = student.get("roll_no", "N/A")
        student_class = student.get("class_name", "B.tech Div A")
        attendance = student.get("attendance", 0)
        subjects = student.get("subjects", [])
        overall_th = student.get("overall_th", "-")
        overall_pr = student.get("overall_pr", "-")
        
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        header_text = "<b>Department:</b> Computer Engineering       <b>Academic Year:</b> 2025- 2026                    <b>Semester:</b> I /II"
        story.append(Paragraph(header_text, normal_style))
        
        date_text = f"<para align=right><b>Date:</b> {current_date}</para>"
        story.append(Paragraph(date_text, normal_style))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("To,", normal_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Dear Sir/Madam,", normal_style))
        story.append(Spacer(1, 10))
        
        body_para1 = (
            f"We are sorry to inform you that attendance of your ward <b>{student_name}</b> "
            f"PRN No. <b>{student_prn}</b> Year <b>{student_class.split(' ')[0]}</b> Div <b>{' '.join(student_class.split(' ')[1:]) if ' ' in student_class else 'A'}</b> is poor."
        )
        story.append(Paragraph(body_para1, normal_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("1. Subject wise attendance up to date is as follows:", normal_style))
        story.append(Spacer(1, 10))
        
        # Build Table Data
        table_data = [
            ["Sr. No", "Subject", "Theory Attendance (%)", "Practical Attendance (%)"]
        ]
        
        for idx, sub in enumerate(subjects, 1):
            table_data.append([
                str(idx),
                sub.get("name", ""),
                str(sub.get("theory", "")),
                str(sub.get("practical", ""))
            ])
            
        # Add summary rows
        table_data.append(["Average attendance (%)", "", str(overall_th), str(overall_pr)])
        table_data.append(["Total Attendance (%)", "", str(attendance), str(attendance)])
        
        # Table Styling
        t = Table(table_data, colWidths=[50, 200, 130, 140])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('SPAN', (0, -2), (1, -2)), # Span "Average attendance (%)" across two columns
            ('SPAN', (0, -1), (1, -1)), # Span "Total Attendance (%)"
            ('ALIGN', (0, -2), (0, -1), 'RIGHT'), # Align summary text to right
            ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(t)
        story.append(Spacer(1, 15))
        
        warning_text = (
            "If he/she fails to improve attendance and to satisfy to minimum criteria of 75% attendance in theory and "
            "practical's conducted, by college, he/she shall not be eligible to appear for Final SA in Semester I / II Theory Examination."
        )
        story.append(Paragraph(warning_text, normal_style))
        story.append(Spacer(1, 40))
        
        # Signatures table
        sig_data = [
            ["Class Teacher", "Academic Coordinator", "Head of the Department"],
            ["Mr. Ganesh Kadam", "Mr. Atul Pawar", "Dr. Sonali Patil"]
        ]
        sig_table = Table(sig_data, colWidths=[180, 180, 180])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(sig_table)
        story.append(PageBreak())
        
    doc.build(story)
    
    buffer.seek(0)
    return buffer.read()
