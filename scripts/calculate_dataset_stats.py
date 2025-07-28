"""
Script for calculating necessary dataset statistics before fine-tuning XTTS-v2.  
"""

import os 
import librosa 


DATASET_DIR = "/home/maksim/Datasets/TTS/RUSLAN/RUSLAN"


def calculate_dataset_stats():
    audiofiles = os.listdir(DATASET_DIR)

    max_len = -1
    min_len = 10000000000000

    for audiofile in audiofiles:
        audio, sr = librosa.load(DATASET_DIR + '/' + audiofile)

        if sr != 22050:
            raise ValueError(f"Audio {audiofile} has incorrect sr!")
    
        audio_len = len(audio)

        if audio_len > max_len:
            max_len = audio_len
    
        if audio_len < min_len:
            min_len = audio_len

    print(f"Min audio length: {min_len}")
    print(f"Max audio length: {max_len}")


if __name__ == "__main__":
    calculate_dataset_stats()