from serializer_factory import SerializerFactory
def main():
    config_format = "xml"
    try :
        serializer = SerializerFactory.get_serializer(config_format)
        print(serializer.serialize("My business data"))
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
