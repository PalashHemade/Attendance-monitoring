import pandas as pd
import io
import re

def parse_attendance_file(file_bytes: bytes, filename: str):
    if filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(file_bytes), header=None)
    elif filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(file_bytes), header=None)
    else:
        raise ValueError("Unsupported format. Please upload .csv or .xlsx")

    df = df.astype(str)
    df = df.replace(["nan", "NaN", "None"], "")
    
    # Find the header row index (where "Sr.No" is)
    header_idx = -1
    for i, row in df.iterrows():
        if "Sr.No" in str(row.values[0]) or "PRN" in str(row.values[1]):
            header_idx = i
            break
            
    if header_idx == -1:
        raise ValueError("Could not find header row starting with Sr.No or PRN")
        
    headers = df.iloc[header_idx].values
    
    # Fixed mappings according to user instruction
    SUBJECT_MAP = {
        "BCE7418 - CC-\nCP - TH": ("Cloud computing", "TH"),
        "BCE7419 - CCL-\nCP - PR": ("Cloud computing", "PR"),
        "BCE7420 - STQA-\nCP - TH": ("STQA", "TH"),
        "BCE7421 - STQAL-\nCP - PR": ("STQA", "PR"),
        "BCE7515 - BI-\nEL - TH": ("Business Intelligence", "TH"),
        "BCE7520 - NLP-\nEL - TH": ("NLP", "TH"),
        "BME7605B - OE-V IE-\nEL - TH": ("IE", "TH"),
        "BCE7521 - PBL-5-\nCP - PR": ("PBL -5", "PR"),
    }
    
    subjects_info = [] # list of dict: {col_idx, name, type (TH/PR)}
    overall_att_col = -1
    overall_th_col = -1
    overall_pr_col = -1
    prn_col = -1
    name_col = -1
    sr_col = -1
    
    for c, val in enumerate(headers):
        sval = str(val).strip()
        if not sval: continue
        
        if "Sr.No" == sval: sr_col = c
        elif "PRN" == sval: prn_col = c
        elif "Name of the Student" in sval: name_col = c
        elif "Overall Att." == sval: overall_att_col = c
        elif "Overall TH Att." == sval: overall_th_col = c
        elif "Overall PR Att." == sval: overall_pr_col = c
        else:
            # Try to match neatly with the mapped subjects
            for key, (sub_name, sub_type) in SUBJECT_MAP.items():
                if key.replace('\n', '') == sval.replace('\n', ''):
                    subjects_info.append({"col": c, "name": sub_name, "type": sub_type})
                    break

    if overall_att_col == -1:
        # Fallback if names change slightly
        for c, val in enumerate(headers):
            if "Overall Att" in str(val): overall_att_col = c
    if overall_att_col == -1:
        raise ValueError("Could not find 'Overall Att.' column")
        
    defaulters = []
    
    # Parse data starting after header
    for i in range(header_idx + 1, len(df)):
        sr_val = str(df.iloc[i, sr_col]).strip()
        if not sr_val.isdigit():
            continue
            
        prn = str(df.iloc[i, prn_col]).strip()
        name = str(df.iloc[i, name_col]).strip()
        
        overall_str = str(df.iloc[i, overall_att_col]).replace("%", "").strip()
        try:
            overall_att = float(overall_str)
        except ValueError:
            continue
            
        if overall_att < 75.0:
            stu_subjects = {}
            for info in subjects_info:
                # The "Per" (percentage) is 2 columns right of the subject header column
                per_col = info["col"] + 2
                if per_col < len(df.columns):
                    val_str = str(df.iloc[i, per_col]).replace("%", "").strip()
                    if val_str and val_str != "-" and val_str != "nan":
                        if info["name"] not in stu_subjects:
                            stu_subjects[info["name"]] = {"TH": "", "PR": ""}
                        stu_subjects[info["name"]][info["type"]] = val_str
            
            subs_list = []
            for sname, sdata in stu_subjects.items():
                subs_list.append({
                    "name": sname,
                    "theory": sdata.get("TH", ""),
                    "practical": sdata.get("PR", "")
                })
                
            overall_th = str(df.iloc[i, overall_th_col]).replace("%", "").strip() if overall_th_col != -1 else ""
            overall_pr = str(df.iloc[i, overall_pr_col]).replace("%", "").strip() if overall_pr_col != -1 else ""
            if overall_th == "-" or overall_th == "nan": overall_th = ""
            if overall_pr == "-" or overall_pr == "nan": overall_pr = ""
            
            defaulters.append({
                "name": name,
                "roll_no": prn,
                "class_name": "B.tech Div A", 
                "attendance": overall_att,
                "subjects": subs_list,
                "overall_th": overall_th,
                "overall_pr": overall_pr
            })

    return defaulters
