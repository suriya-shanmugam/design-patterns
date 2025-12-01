class AppConfig :
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None :
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized :
            return
        print("Loading from files...")
        # Parsing logic goes here
        
        self.url = "https://localhost:4999"
        self.user_name = "suriya"
        self._initialized = True

config1 = AppConfig()
config2 = AppConfig()
print("Is both reference pointing to same memory location - ", config1 is config2)

