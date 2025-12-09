from serializer import Serializer

class XmlSerializer(Serializer):
    def serialize(self, data):
        return f"XML representation: <data>{data}</data>"
