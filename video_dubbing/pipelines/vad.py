import torch
import numpy as np

from video_dubbing.core import ProcessingContext, DubbingSegment
from video_dubbing.core import VADProcessor


class SileroVADProcessor(VADProcessor):
    def __init__(self, model_path: str = "", threshold: float = 0.5,  
                  min_silence_duration_ms=1000, 
                  min_speech_duration_ms=1000):
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

        self.threshold = threshold
        self.min_silence_duration_ms = min_silence_duration_ms
        self.min_speech_duration_ms = min_speech_duration_ms


    def __call__(self, context: ProcessingContext) -> ProcessingContext:
        speech_audio = []
        new2old = {}
    
        speech_timestamps = self.get_speech_timestamps(context.original_audio, 
                                                  self.silerovad, 
                                                  threshold=self.threshold, 
                                                  sampling_rate=context.sample_rate,
                                                  min_silence_duration_ms=self.min_silence_duration_ms, 
                                                  min_speech_duration_ms=self.min_speech_duration_ms)
    
        for ts in speech_timestamps:
            start = ts['start']
            end = ts['end']
            context.segments.append(DubbingSegment(start=start, 
                                                 end=end, 
                                                 audio=context.original_audio[start:end]))


        start_idx = 0

        for segment in context.segments:
            new2old[(start_idx, segment.end - segment.start + start_idx)] = segment

            start_idx = segment.end - segment.start + start_idx + 1

            speech_audio.extend(segment.audio.tolist())

        context.speech_audio = np.array(speech_audio)
        context.timestamps_mapping = new2old
        
        return context 