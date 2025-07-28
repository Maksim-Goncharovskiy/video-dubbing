import os
from abc import ABCMeta, abstractmethod

import torch 
import numpy as np

import soundfile as sf
from TTS.api import TTS

from .segment import Segment


class TTSPipeline(metaclass=ABCMeta):
    @abstractmethod
    def _process_sample(self, audio: str) -> np.ndarray:
        pass
    

    @abstractmethod
    def __call__(self, texts_ru: list[Segment], *args, **kwargs) -> list[Segment]:
        pass




class XTTSPipeline(TTSPipeline):
    output_sampling_rate = 24_000

    def __init__(self, target_spk: str | None = None, model_path: str | None = None, device: str = 'cpu', temp_dir="./temp-dir/tts/"):
        self.target_spk = target_spk

        if model_path:
            self.model = TTS(model_path=model_path, config_path=f'{model_path}/config.json').to(device)
        else:
            self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

        self.temp_dir = temp_dir


    def _process_sample(self, text_ru: str, speaker_wav: str) -> np.ndarray:
        return self.model.tts(text=text_ru, speaker_wav=speaker_wav, language='ru')


    def __call__(self, segments: list[Segment]) -> list[Segment]:
        os.makedirs(self.temp_dir, exist_ok=True)

        for i, segment in enumerate(segments):
            if self.target_spk is None:
                audio_path = self.temp_dir + f"{i}.wav"

                sf.write(audio_path, segment.audio, 16_000)

                segment.tts_wav = self._process_sample(segment.translation, audio_path)

                os.remove(audio_path)
            else:
                segment.tts_wav = self._process_sample(segment.translation, self.target_spk)

        return segments



class SileroTTSPipeline(TTSPipeline):
    output_sampling_rate = 48_000

    def __init__(self, model_path: str | None = None, device: str = 'cpu'):
        if model_path:
            self.silero_tts, _ = torch.hub.load(repo_or_dir=model_path,
                                     model='silero_tts',
                                     language='ru',
                                     speaker='v4_ru',
                                     source='local')

        else:
            self.silero_tts, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language='ru',
                                     speaker='v4_ru',
                                     source='github')
        
        self.silero_tts.to(device)


    def _process_sample(self, text_ru: str, speaker: str) -> np.ndarray:
        return self.silero_tts.apply_tts(text=text_ru,
                        speaker=speaker,
                        sample_rate=self.output_sampling_rate).numpy()


    def __call__(self, segments: list[Segment], speaker: str = "xenia"):
        for segment in segments:
            segment.tts_wav = self._process_sample(segment.translation, speaker)