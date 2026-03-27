import pandas as pd
import io

def parse_attendance_file(file_bytes: bytes, filename: str):
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_bytes))
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(file_bytes))
        else:
            raise ValueError("Unsupported file format. Please upload .csv or .xlsx")
        
        # Normalize column names to lower case without extra spaces for flexible matching
        original_cols = df.columns.tolist()
        df.columns = df.columns.str.strip().str.lower()
        
        # Locate the attendance column
        attendance_col = None
        for col in df.columns:
            if "attendance" in col:
                attendance_col = col
                break
        
        if not attendance_col:
            raise ValueError("Could not find an 'Attendance' column in the file.")
            
        name_col = next((c for c in df.columns if "name" in c), None)
        roll_col = next((c for c in df.columns if "roll" in c), None)
        class_col = next((c for c in df.columns if "class" in c or "div" in c), None)
        
        if not name_col:
            raise ValueError("Could not find a 'Name' column in the file.")
            
        # Filter defaulters
        # Convert attendance to numeric in case there's '%' sign
        if df[attendance_col].dtype == object:
            df[attendance_col] = df[attendance_col].astype(str).str.replace("%", "").astype(float)
            
        defaulters_df = df[df[attendance_col] < 75]
        
        defaulters = []
        for _, row in defaulters_df.iterrows():
            defaulters.append({
                "name": row[name_col] if name_col else "Unknown",
                "roll_no": row[roll_col] if roll_col and not pd.isna(row[roll_col]) else "N/A",
                "class_name": row[class_col] if class_col and not pd.isna(row[class_col]) else "N/A",
                "attendance": row[attendance_col]
            })
            
        return defaulters
    except Exception as e:
        raise Exception(f"Error parsing file: {str(e)}")
