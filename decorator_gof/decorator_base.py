from simple_textpublisher import TextPublisher

class TextDecorator(TextPublisher):
    def __init__(self, component:TextPublisher):
        self._component = component

    def publish(self):
        return self._component.publish()


