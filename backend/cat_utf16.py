with open("inspect_out.txt", "r", encoding="utf-16le") as f:
    text = f.read()
with open("inspect_out_utf8.txt", "w", encoding="utf-8") as f:
    f.write(text)
