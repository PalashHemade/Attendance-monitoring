from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from typing import List
from pydantic import BaseModel
import uvicorn

from services.file_parser import parse_attendance_file
from services.letter_generator import generate_defaulter_letters

app = FastAPI(title="Attendance Defaulter API")

# Setup CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Student(BaseModel):
    name: str
    roll_no: str | int | float
    class_name: str
    attendance: float

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Only .csv and .xlsx files are supported")
    
    try:
        contents = await file.read()
        defaulters = parse_attendance_file(contents, file.filename)
        return {"defaulters": defaulters}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate-letters")
async def generate_letters(defaulters: List[Student]):
    try:
        students_dict = [d.model_dump() for d in defaulters]
        pdf_bytes = generate_defaulter_letters(students_dict)
        return Response(content=pdf_bytes, media_type="application/pdf", headers={
            "Content-Disposition": "attachment; filename=defaulter_letters.pdf"
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating PDF: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
