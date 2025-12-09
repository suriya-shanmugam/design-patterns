from serializer import Serializer

class JsonSerializer(Serializer):
    def serialize(self, data):
        return f"JSON representation : {{'data':'{data}'}}"

