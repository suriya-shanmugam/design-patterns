from textpublisher_base import TextPublisher

class SimpleText(TextPublisher):
    def __init__(self, text:str):
        self._text = text
    
    def publish(self):
        return self._text
