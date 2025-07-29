from dataclasses import dataclass, field
import numpy as np


@dataclass
class DubbingSegment:
    start: int = field(repr=True) # Начало сегмента (индекс в исходном аудио)
    end: int = field(repr=True) # Конец сегмента
    audio: np.ndarray = field(repr=False) # Аудио сегмент

    transcription: str = field(repr=True, default=None)
    translation: str = field(repr=True, default=None)

    tts_wav: np.ndarray = field(repr=False, default=None)


@dataclass
class ProcessingContext:
    original_audio: np.ndarray = field(repr=False)
    sample_rate: int = field(repr=True)
    temp_dir: str = field(repr=True) # директория, куда будут сохраняться временные файлы в процессе обработки

    segments: list[DubbingSegment] = field(default_factory=list, repr=False)

    speech_audio: np.ndarray = field(repr=False, default=None)

    # соответствие временных отрезков между original_audio и speech_audio
    timestamps_mapping: dict[tuple[int, int], DubbingSegment] = field(repr=False, default=None) 