import sys
import pandas as pd

try:
    df = pd.read_excel(r"d:\Avengers Doomsday\Assignment-6\Attendance_Report_37.xlsx", header=None)
    
    # Try to find exactly where the headers start
    print("--- FIRST 30 ROWS ---")
    for i, row in df.head(30).iterrows():
        print(f"Row {i}: {row.values}")

except Exception as e:
    print("Error:", e)
