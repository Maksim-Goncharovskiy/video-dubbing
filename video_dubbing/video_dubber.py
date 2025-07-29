# Здесь будет главный класс-интерфейс-обработчик!
import os 

import torch 
import torchaudio
import numpy as np
from moviepy import VideoFileClip, AudioFileClip
import soundfile as sf
import ffmpeg

from video_dubbing.core import ProcessingContext


class VideoDubber:
    def __init__(self, config: dict):
        self.processors = []

        for processor in config["pipeline"]:
            self.processors.append(processor.model(**processor.params))
        
        self.temp_dir = config["temp-dir"]
    

    def _extract_audio_from_mp4(self, 
                                video_path: str, 
                                target_sr: int = 16000) -> tuple[np.ndarray, int]:
        
        video = VideoFileClip(video_path)
        audio: AudioFileClip = video.audio

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        temp_audio_path = self.temp_dir + "original_audio.wav"
        audio.write_audiofile(temp_audio_path, codec='pcm_s16le', fps=target_sr)
    
        audio_data, sr = torchaudio.load(temp_audio_path)
    
        if sr != target_sr:
            audio_data = torchaudio.transforms.Resample(orig_freq=sr, new_freq=target_sr)(audio_data)
    
        if audio_data.shape[0] > 1:
            audio_data = audio_data.mean(dim=0)

        os.remove(temp_audio_path)
    
        return audio_data.numpy(), sr


    def _merge_audio_video(self, audio: np.ndarray, sr: int, video_path: str, output_path: str):
        audio_path = self.temp_dir + "/output.wav"

        sf.write(audio_path, audio, 16_000)

        video = ffmpeg.input(video_path).video
        audio = ffmpeg.input(audio_path).audio

        ffmpeg.output(audio, video, output_path, vcodec="copy", acodec="aac").run()

        os.remove(audio_path)
    

    def _merge_segments_with_alignment(self, context: ProcessingContext) -> np.ndarray:
        orig_audio_len = len(context.original_audio)
        output_audio = np.array([0.0] * orig_audio_len)
    
        tts_sr = self.processors[-1].output_sample_rate

        for segment in context.segments:
            segment_len = segment.end - segment.start
            tts_wav = torchaudio.transforms.Resample(orig_freq=tts_sr, new_freq=context.sample_rate)(torch.tensor(segment.tts_wav)).numpy()

            if len(tts_wav) < segment_len:
                output_audio[segment.start:segment.start+len(tts_wav)] = tts_wav
            else:
                output_audio[segment.start:segment.end] = tts_wav[:segment_len]

        return output_audio


    def __call__(self, input_video_path: str, output_video_path: str):
        os.makedirs(self.temp_dir, exist_ok=True)

        audio, sr = self._extract_audio_from_mp4(input_video_path, target_sr=16_000)

        context = ProcessingContext(original_audio=audio, sample_rate=sr, temp_dir=self.temp_dir)

        for processor in self.processors:
            context = processor(context)
        
        output_audio = self._merge_segments_with_alignment(context=context)

        self._merge_audio_video(output_audio, sr, input_video_path, output_video_path)
        
        os.rmdir(self.temp_dir)