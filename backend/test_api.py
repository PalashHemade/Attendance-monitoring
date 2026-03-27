import requests
import json

url = "http://localhost:8000/upload"
filepath = r"d:\Avengers Doomsday\Assignment-6\Attendance_Report_37.xlsx"

try:
    with open(filepath, "rb") as f:
        files = {"file": ("Attendance_Report_37.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        response = requests.post(url, files=files)
        
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        defs = data.get("defaulters", [])
        print(f"Successfully parsed! {len(defs)} defaulters found.")
        if defs:
            print(json.dumps(defs[0], indent=2))
            
            # Now test PDF generation
            pdf_url = "http://localhost:8000/generate-letters"
            pdf_resp = requests.post(pdf_url, json=defs[:2]) # test with first 2
            
            if pdf_resp.status_code == 200:
                print("PDF generated successfully, length:", len(pdf_resp.content))
                with open(r"d:\Avengers Doomsday\Assignment-6\backend\test_defaulter.pdf", "wb") as pf:
                    pf.write(pdf_resp.content)
                print("Saved PDF locally to test_defaulter.pdf")
            else:
                print("PDF Error:", pdf_resp.text)
    else:
        print("Error:", response.text)
except Exception as e:
    print("Exception:", e)
