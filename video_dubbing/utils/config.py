from video_dubbing.pipelines import SileroTTSProcessor, FasterWhisperProcessor, SileroVADProcessor, HelsinkiEnRuProcessor
from dataclasses import dataclass, field

@dataclass
class ProcessorConfig:
    stage: str = field(repr=True)
    model: type = field(repr=True)
    params: dict = field(repr=True)


cpu_config = {
    "pipeline": [
        ProcessorConfig(
            stage="vad",
            model=SileroVADProcessor,
            params={
                "model_path": "/home/maksim/Models/SileroVAD/snakers4-silero-vad", 
                "threshold": 0.5,  
                "min_silence_duration_ms": 1000, 
                "min_speech_duration_ms": 1000
            }
        ),
        ProcessorConfig(
            stage="asr",
            model=FasterWhisperProcessor,
            params={
                "model_size_or_path": "/home/maksim/Models/FasterWhisper/tiny-en", 
                "device": "cpu", 
                "compute_type": "int8"
            }
        ), 
        ProcessorConfig(
            stage="mt",
            model=HelsinkiEnRuProcessor,
            params={
                "model_path": "/home/maksim/Models/OpusEnRu", 
                "device": 'cpu'
            }
        ),  
        ProcessorConfig(
            stage="tts",
            model=SileroTTSProcessor,
            params={
                "model_path": "/home/maksim/Models/SileroModels", 
                "device": 'cpu', 
                "speaker": "xenia"
            }
        )
    ],
    "temp-dir": "./video-dubbing-temp-dir"}


def load_config():
    pass 