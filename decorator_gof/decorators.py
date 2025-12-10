from decorator_base import TextDecorator

class HTMLDecorator(TextDecorator):
    def publish(self):
        return f"<html>{super().publish()}</html>"

class UpperCaseDecorator(TextDecorator):
    def publish(self):
        return super().publish().upper()
