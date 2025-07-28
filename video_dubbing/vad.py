from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field

import torch
import numpy as np

from .segment import Segment



@dataclass
class VadOutput:
    segments: list[Segment] = field(repr=False)
    audio: np.ndarray = field(repr=False)
    timestamps_mapping: dict[tuple[int, int], Segment] = field(repr=False)



class VADPipeline(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, audio, *args, **kwargs) -> VadOutput:
        pass



class SileroVADPipeline(VADPipeline):
    def __init__(self, model_path: str = ""):
        """
        Для локальной загрузки модели, нужно сначала её скачать: git clone <silerovad repo>
        А затем передать в качестве параметра model_path путь до корня склонированного репозитория.
        """
        if model_path:
            self.silerovad, utils = torch.hub.load(repo_or_dir=model_path,
                              model='silero_vad',
                              force_reload=True,
                              source='local')
        else:
            self.silerovad, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                model='silero_vad',
                                force_reload=True, 
                                source='github') 

        (self.get_speech_timestamps, _, _, _, _) = utils


    def __call__(self,
                  audio: np.ndarray, 
                  threshold: float = 0.5,  
                  min_silence_duration_ms=1000, 
                  min_speech_duration_ms=1000, 
                  sampling_rate=16000) -> VadOutput:
        
        speech_segments: list[Segment] = []
        speech_audio = []
        new2old = {}
    
        speech_timestamps = self.get_speech_timestamps(audio, 
                                                  self.silerovad, 
                                                  threshold=threshold, 
                                                  sampling_rate=sampling_rate,
                                                  min_silence_duration_ms=min_silence_duration_ms, 
                                                  min_speech_duration_ms=min_speech_duration_ms)
    
        for ts in speech_timestamps:
            start = ts['start']
            end = ts['end']
            speech_segments.append(Segment(start=start, end=end, audio=audio[start:end]))


        start_idx = 0

        for segment in speech_segments:
            new2old[(start_idx, segment.end - segment.start + start_idx)] = segment

            start_idx = segment.end - segment.start + start_idx + 1

            speech_audio.extend(segment.audio.tolist())

        speech_audio = np.array(speech_audio)

        output: VadOutput = VadOutput(segments=speech_segments, audio=speech_audio, timestamps_mapping=new2old)
        
        return output