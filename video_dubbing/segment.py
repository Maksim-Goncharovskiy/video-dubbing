from dataclasses import dataclass, field

import numpy as np



@dataclass
class Segment:
    start: int = field(repr=True) # Начало сегмента (индекс в исходном аудио)
    end: int = field(repr=True) # Конец сегмента

    audio: np.ndarray = field(repr=False) # Аудио сегмент

    audio_path: str = field(repr=True, default=None) # Путь до аудиофайла, если таковой имеется (для XTTS)

    transcription: str = field(repr=True, default=None) # Транскрипция сегмента
    translation: str = field(repr=True, default=None) # Перевод сегмента

    tts_wav: np.ndarray = field(repr=False, default=None) # Озвучка (numpy.ndarray)