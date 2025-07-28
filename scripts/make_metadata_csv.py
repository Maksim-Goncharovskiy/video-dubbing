"""
Script for processing json file with labels from label-studio to ljspeech metadata.csv format.
"""

import json

# WRITE HERE A PATH TO YOUR JSON-FILE WITH LABELS (from label-studio)
JSON_PATH = "/home/maksim/Repos/video_dubbing/labels.json"


def make_metadata_csv():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    metadata = []
    for item in data:
        audio_name: str = item["audio"].split(".")[0]
        name_start_idx = audio_name.find("MG-")
        audio_name = audio_name[name_start_idx:]

        text1 = item["transcription-1"]
        text2 = item["transcription-2"]

        metadata.append(f"{audio_name}|{text1}|{text2}")

    with open('./metadata.csv', 'w', encoding='utf-8') as file:
        for line in metadata:
            file.write(line + '\n') 


if __name__ == "__main__":
    make_metadata_csv()