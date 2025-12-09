from json_serializer import JsonSerializer
from xml_serializer import XmlSerializer
class SerializerFactory():
    @staticmethod
    def get_serializer(format_type):
        if format_type == 'json':
            return JsonSerializer()
        elif format_type == 'xml':
            return XmlSerializer()
        else :
            raise ValueError(f"Unknown foramt:{format_type}")

