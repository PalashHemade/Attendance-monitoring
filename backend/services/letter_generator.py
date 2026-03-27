import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_defaulter_letters(defaulters: list) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    for student in defaulters:
        student_name = student.get("name", "Unknown")
        student_class = student.get("class_name", "N/A")
        attendance = student.get("attendance", 0)
        
        # Draw the letter
        textobject = c.beginText()
        textobject.setTextOrigin(inch, height - inch * 2)
        textobject.setFont("Helvetica", 12)
        textobject.setLeading(20)
        
        lines = [
            "Date: [Current Date]",
            "",
            "Dear Parent,",
            "",
            f"This is to inform you that your ward, {student_name},",
            f"studying in {student_class}, has an attendance of {attendance}%,",
            "which is below the required minimum of 75%.",
            "",
            "You are requested to ensure regular attendance to avoid",
            "any academic penalties.",
            "",
            "Sincerely,",
            "Class Teacher"
        ]
        
        for line in lines:
            textobject.textLine(line)
            
        c.drawText(textobject)
        c.showPage() # End the current page
        
    c.save()
    buffer.seek(0)
    return buffer.read()
