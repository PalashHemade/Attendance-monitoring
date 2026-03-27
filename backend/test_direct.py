from services.file_parser import parse_attendance_file
from services.letter_generator import generate_defaulter_letters

filepath = r"d:\Avengers Doomsday\Assignment-6\Attendance_Report_37.xlsx"
with open(filepath, "rb") as f:
    contents = f.read()

try:
    defs = parse_attendance_file(contents, "Attendance_Report_37.xlsx")
    print(f"Parsed {len(defs)} defaulters.")
    if defs:
        print("First:", defs[0])
        pdf_bytes = generate_defaulter_letters(defs[:2]) # test 2 letters
        with open("test_letters.pdf", "wb") as pf:
            pf.write(pdf_bytes)
        print("Generated test_letters.pdf successfully.")
except Exception as e:
    import traceback
    traceback.print_exc()
