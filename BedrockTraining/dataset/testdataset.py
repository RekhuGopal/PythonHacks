import json
with open("train.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        print(f"Line {i}:", line.strip())