import torch
import torchaudio
from faster_whisper import WhisperModel, BatchedInferencePipeline
from video_dubbing.core import ProcessingContext, DubbingSegment
from video_dubbing.core import ASRProcessor


class FasterWhisperProcessor(ASRProcessor):
    sr = 16_000

    def __init__(self, model_size_or_path: str = "tiny.en", device: str = "cpu", compute_type: str = "int8", batch_size=8):
        self.model = model=WhisperModel(model_size_or_path=model_size_or_path,
                                                                  device=device, 
                                                                  compute_type=compute_type)
        self.batch_size = batch_size
        self.last_segment: DubbingSegment | None = None


    def _put_word_in_segment(self, word: str, start: int, end: int, context: ProcessingContext):
        word_processed: bool = False

        for ts_interval in context.timestamps_mapping.keys():
            if start >= ts_interval[0] and end <= ts_interval[1]:
                segment = context.timestamps_mapping[ts_interval]
                if segment.transcription:
                    segment.transcription += word
                else:
                    segment.transcription = word

                word_processed = True
                self.last_segment = segment

                break 

        if not(word_processed):
            self.last_segment.transcription += word
        
        return context

    
    def __call__(self, context: ProcessingContext) -> ProcessingContext:
        speech_audio = context.speech_audio

        if context.sample_rate != self.sr:
            speech_audio = torchaudio.transforms.Resample(orig_freq=context.sample_rate,
                                                           new_freq=self.sr)(torch.tensor(speech_audio)).numpy()

        whisper_segments, _ = self.model.transcribe(context.speech_audio, word_timestamps=True)
        
        for segment in whisper_segments:
            for word in segment.words:
                context = self._put_word_in_segment(word=word.word,
                                           start=int(word.start * self.sr), 
                                           end=int(word.end * self.sr), 
                                           context=context)

        return context