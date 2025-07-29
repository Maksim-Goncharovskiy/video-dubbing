from abc import ABC, abstractmethod
from .models import ProcessingContext


class BaseProcessor(ABC):
    @abstractmethod
    def __call__(self, context: ProcessingContext) -> ProcessingContext:
        pass


class VADProcessor(BaseProcessor):
    pass


class ASRProcessor(BaseProcessor):
    pass


class MTProcessor(BaseProcessor):
    pass


class TTSProcessor(BaseProcessor):
    pass