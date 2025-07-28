"""
Script for preprocessing RUSLAN TTS dataset before fine-tuning XTTS-v2 model.
Preprocessing includes:
    - removing too long audios (> 12s)
    - adding a second transcription column to the metadata.csv

! IMPORTANT: 
YOUR ORIGINAL DATASET FILES WILL BE PROCESSED (long audios will be deleted from your dataset folder and metadata.csv will be changed).
SO IF YOU WANT TO SAVE ORIGINAL RUSLAN DATASET VERSION, PLEASE, MAKE A COPY. 
"""

import os 
import librosa 
import pandas as pd


DATASET_DIR = "/home/maksim/Datasets/TTS/RUSLAN/RUSLAN" # path to wavs
PATH_TO_METADATA = "/home/maksim/Datasets/TTS/RUSLAN/metadata_RUSLAN_22200.csv"


def process_ruslan_dataset():
    metadata = pd.read_csv(PATH_TO_METADATA, sep="|", header=None, index_col=0)

    audiofiles = os.listdir(DATASET_DIR)

    for audiofile in audiofiles:
        audiofile_path = DATASET_DIR + '/' + audiofile

        audio, sr = librosa.load(audiofile_path)

        if sr != 22050:
            raise ValueError(f"Audio {audiofile} has incorrect sr!")
    
        if len(audio) / sr > 12:
            os.remove(audiofile_path)
            metadata = metadata.drop([audiofile.split('.')[0]], axis=0)

    metadata[2] = metadata[1].values

    metadata.to_csv(PATH_TO_METADATA, sep='|')


if __name__ == "__main__":
    process_ruslan_dataset()