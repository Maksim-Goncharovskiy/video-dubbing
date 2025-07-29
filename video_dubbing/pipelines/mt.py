from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

from video_dubbing.core import ProcessingContext, DubbingSegment
from video_dubbing.core import MTProcessor


class HelsinkiEnRuProcessor(MTProcessor):
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


    def __call__(self, context: ProcessingContext) -> ProcessingContext:
        for segment in context.segments:
            segment.translation = self._process_sample(segment.transcription)
        
        return context