from abc import ABCMeta, abstractmethod

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

from .segment import Segment



class MTPipeline(metaclass=ABCMeta):
    @abstractmethod
    def _process_sample(self, text_en: str) -> str:
        pass


    @abstractmethod
    def __call__(self, texts_en: list[Segment]) -> list[Segment]:
        pass



class HelsinkiEnRuPipeline(MTPipeline):
    def __init__(self, model_path: str | None = None, device: str = 'cpu'):
        model = None
        tokenizer = None 
        if model_path:
            model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
            tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        else:
            model_hf_name = "Helsinki-NLP/opus-mt-en-ru"
            model = AutoModelForSeq2SeqLM.from_pretrained(model_hf_name)
            tokenizer = AutoTokenizer.from_pretrained(model_hf_name)
        
        self.pipe = pipeline(
            task="translation", 
            model=model, 
            tokenizer=tokenizer,
            device=device)

    def _process_sample(self, text_en: str) -> str:
        return self.pipe(text_en)[0]['translation_text']


    def __call__(self, segments: list[Segment]):
        for segment in segments:
            segment.translation = self._process_sample(segment.transcription)