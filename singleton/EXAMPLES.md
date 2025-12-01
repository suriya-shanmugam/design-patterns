### The Two Ways to Implement Singletons in Python

#### 1\. The "Pythonic" Way (Modules)

In Python, modules are Singletons by design. When you import a module for the first time, Python initializes it. Subsequent imports return the *same* module object.

```python
# config.py
settings = {
    "db": "postgres",
    "host": "localhost"
}

# main.py
import config
print(config.settings) # This uses the single instance created by the runtime
```

*Use this for simple shared state.*

#### 2\. The Object-Oriented Way (Using `__new__`)

If you need a Class (for inheritance, properties, etc.), you override the `__new__` method. This method is called *before* `__init__` to create the instance.

-----

### Real World Use Case 1: Application Configuration Manager

**Scenario:** You have a complex application (like a Flask or Django app) that needs to read environment variables or a YAML config file. You do not want to re-read the disk and parse the file every time you need to check a setting.

**Implementation:**

```python
import os

class AppConfig:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the instance if it doesn't exist
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # We check _initialized to ensure we don't reload config 
        # every time 'AppConfig()' is called.
        if self._initialized:
            return
            
        print("Loading configuration from file...")
        # Simulating loading heavy config
        self.database_url = os.getenv("DB_URL", "sqlite:///prod.db")
        self.debug_mode = True
        self._initialized = True

# Usage
config1 = AppConfig()
print(f"Config 1 DB: {config1.database_url}")

config2 = AppConfig() # Does NOT print "Loading configuration..."
print(f"Config 2 DB: {config2.database_url}")

print(config1 is config2) # True (They are the same object)
```

-----

### Real World Use Case 2: Database Connection Wrapper

**Scenario:** Creating a database connection is expensive (networking, authentication handshake). You generally want one shared connection (or a pool manager) rather than opening a new socket for every query.

**Implementation (Thread-Safe):**
In a multi-threaded environment (like a web server), two threads might try to create the Singleton at the exact same millisecond. We use a **Lock** to prevent this.

```python
import threading
import sqlite3

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock() # Class-level lock

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking pattern
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Ensure connection is only opened once
        if not hasattr(self, 'connection'):
            print("Opening connection to Database...")
            self.connection = sqlite3.connect(':memory:')
            self.cursor = self.connection.cursor()

    def query(self, sql):
        return self.cursor.execute(sql).fetchall()

# Usage
db1 = DatabaseConnection()
db1.query("CREATE TABLE users (id INTEGER, name TEXT)")
db1.query("INSERT INTO users VALUES (1, 'Alice')")

# Somewhere else in the code...
db2 = DatabaseConnection() 
results = db2.query("SELECT * FROM users") # Reuses the existing connection

print(results) 
# Output: [(1, 'Alice')]
```

-----

### When to Avoid the Singleton

While useful, Singletons are often called an "Anti-Pattern" if overused.

1.  **Testing Difficulties:** Because Singletons hold global state, tests can "leak" into each other. (e.g., Test A changes the Config Singleton, causing Test B to fail).
2.  **Hidden Dependencies:** It is not obvious from looking at a function signature that it relies on a global Singleton inside.

### Summary

  * **Use Modules** for simple global data.
  * **Use the Class pattern** when you need lazy initialization or strict object-oriented control (like DB connections).
  * **Always use Locks** if your application is multi-threaded.
