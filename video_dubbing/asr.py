from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field

import numpy as np
from faster_whisper import WhisperModel



@dataclass
class AsrWordOutput:
    start: int = field(repr=True)
    end: int = field(repr=True)
    word: str = field(repr=True)



class ASRPipeline(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, audio) -> list[AsrWordOutput]:
        pass



class FasterWhisperPipeline(ASRPipeline):
    sr = 16_000

    def __init__(self, model_size_or_path: str = "tiny.en", device: str = "cpu", compute_type: str = "int8"):
        self.model = WhisperModel(model_size_or_path=model_size_or_path, device=device, compute_type=compute_type)
    
    def __call__(self, audio: np.ndarray) -> list[AsrWordOutput]:
        output = []

        segments, _ = self.model.transcribe(audio, word_timestamps=True)
        
        for segment in segments:
            for word in segment.words:
                output.append(
                    AsrWordOutput(
                        start=int(word.start * self.sr), 
                        end=int(word.end * self.sr), 
                        word=word.word
                    )
                )
        
        return output