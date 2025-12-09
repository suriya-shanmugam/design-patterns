### **Pattern \#2: The Factory Method**
#### **The Core Concept**

The Factory Method provides an interface for creating objects in a superclass but allows  dedicated factory function to alter the type of objects that will be created.

Think of it as a **"Virtual Constructor."** Instead of calling `new Object()`, you call `factory.create_object()`.

#### **Scenario & Situation**

You apply this when your program cannot anticipate the class of objects it must create.

**Common Scenarios:**

1.  **Data Export:** Your user wants to download a report. They might choose PDF, CSV, or Excel. You don't know which one they will pick until the app is running.
2.  **Payment Processing:** You accept payments via Stripe, PayPal, or Crypto. The checkout flow is the same ("process payment"), but the underlying object creation differs for each gateway.
3.  **Cross-Platform UI:** If you are running on Windows, create a `WindowsButton`. If on Mac, create a `MacButton`.

#### **What Goes Wrong If NOT Used?**

If you don't use a Factory, you end up with **Tight Coupling** and **Conditional Spaghetti**.

  * **The "Import Hell" Problem:** Your main application code has to import `PDFExporter`, `CSVExporter`, `ExcelExporter`, etc.
  * **The "Modification" Problem:** Every time you add a new format (e.g., XML), you have to go into your core logic, add another `elif format == 'xml': ...`, and risk breaking existing code. This violates the **Open/Closed Principle** (code should be open for extension, but closed for modification).

-----

#### **Python Implementation**

Let's build a **Data Serializer**. Imagine we need to convert an object into either JSON or XML depending on user input.

```python
from abc import ABC, abstractmethod

# 1. The Interface (Product)
# All final objects must follow this blueprint so the client knows what methods to call.
class Serializer(ABC):
    @abstractmethod
    def serialize(self, data):
        pass

# 2. Concrete Products
# These are the actual objects we want to create.
class JsonSerializer(Serializer):
    def serialize(self, data):
        return f"JSON Representation: {{ 'data': '{data}' }}"

class XmlSerializer(Serializer):
    def serialize(self, data):
        return f"XML Representation: <data>{data}</data>"

# 3. The Factory
# This encapsulates the logic of instantiation.
class SerializerFactory:
    @staticmethod
    def get_serializer(format_type):
        if format_type == 'json':
            return JsonSerializer()
        elif format_type == 'xml':
            return XmlSerializer()
        else:
            raise ValueError(f"Unknown format: {format_type}")

# --- Client Code ---

def main():
    # The client doesn't need to import JsonSerializer or XmlSerializer directly.
    # It just deals with the Factory and the common interface.
    
    config_format = "json"  # Imagine this comes from a config file or user input
    
    try:
        # Ask the factory for the object
        serializer = SerializerFactory.get_serializer(config_format)
        
        # Use the object (Polymorphism)
        print(serializer.serialize("My Business Data"))
        
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
```

**Output Analysis:**

1.  The `main` function (the client) has **no idea** that `JsonSerializer` class even exists.
2.  It simply asks the Factory: "Give me something that handles 'json'."
3.  If we want to add a YAML format later, we simply create `YamlSerializer` and update the `SerializerFactory`. We **do not touch** the `main` function logic.

#### **Perks of the Factory Method**

  * **Decoupling:** Separation of concerns. The code that *uses* the object is separated from the code that *creates* the object.
  * **Flexibility:** You can introduce new types of products into the program without breaking existing client code.
  * **Single Responsibility:** You move the complex object creation code to one specific place (the factory), making the code easier to support.

-----

## Additional Reading

---

# Abstract Classes and Interfaces in Python

Python does not have interfaces as a separate language feature. Instead, it implements interface-like behavior using **abstract base classes (ABCs)** from the `abc` module.

---

# 1. Abstract Classes

An **abstract class** is a class that cannot be instantiated. It may contain abstract methods that must be implemented by all subclasses.

## Key Points

* Defined by inheriting from `ABC` (from `abc` module).
* Contains one or more methods marked with `@abstractmethod`.
* Cannot be instantiated unless all abstract methods are implemented in a child class.
* Can contain normal (concrete) methods as well.

## Basic Example

```python
from abc import ABC, abstractmethod

class Shape(ABC):

    @abstractmethod
    def area(self):
        pass

    def description(self):
        return "This is a geometric shape."

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

c = Circle(5)
print(c.area())          # Works
print(c.description())   # Inherited concrete method
```

---

# 2. Abstract Methods

An **abstract method** is a method declared in an abstract class that must be implemented in subclasses.

## Rules

* Decorated with `@abstractmethod`.
* Cannot have an implementation (though Python allows optional default behavior).
* All subclasses must implement every abstract method or they remain abstract.

## Example with multiple abstract methods

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class Car(Vehicle):
    def start(self):
        print("Car started")

    def stop(self):
        print("Car stopped")
```

---

# 3. Interfaces in Python

Python has no dedicated `interface` keyword. Instead, ABCs can be used as **interfaces** by defining a class with only abstract methods and no concrete implementation.

## Interface-like Example

```python
from abc import ABC, abstractmethod

class IStream(ABC):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, data):
        pass

class FileStream(IStream):
    def read(self):
        return "File data"

    def write(self, data):
        print("Writing to file:", data)
```

This functions like an interface: it enforces a contract without any implementation.

---

# 4. Abstract Properties, Class Methods, and Static Methods

The `abc` module allows marking properties and class/static methods as abstract.

## Abstract Property Example

```python
from abc import ABC, abstractmethod

class Person(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

class Student(Person):
    @property
    def name(self):
        return "Alice"
```

## Abstract Class Method Example

```python
from abc import ABC, abstractmethod

class Loader(ABC):

    @classmethod
    @abstractmethod
    def load(cls):
        pass

class JSONLoader(Loader):
    @classmethod
    def load(cls):
        return {"result": "loaded"}
```

## Abstract Static Method Example

```python
from abc import ABC, abstractmethod

class Utils(ABC):

    @staticmethod
    @abstractmethod
    def validate(num):
        pass

class NumberUtils(Utils):

    @staticmethod
    def validate(num):
        return num >= 0
```

---

# 5. Virtual Subclasses

You can register a class as a virtual subclass of an ABC.
This means it will be recognized as a subclass without actually inheriting.

```python
from abc import ABC

class Animal(ABC):
    pass

class Dog:
    pass

Animal.register(Dog)

print(issubclass(Dog, Animal))   # True
print(isinstance(Dog(), Animal)) # True
```

Useful when you want to enforce "duck typing" compatibility without inheritance.

---

# 6. When to Use Abstract Classes vs Interfaces

## Use an abstract class when:

* You want to provide partial implementation.
* You want to share state or common behaviors.
* You want a base class that should not be instantiated.

## Use an interface (ABC with only abstract methods) when:

* You want to enforce a contract without providing implementation.
* You want multiple unrelated classes to follow the same method signature.
* You want a purely behavioral specification.

---

# 7. Multiple Inheritance with Interfaces

Python supports multiple inheritance, so you can implement multiple interfaces.

```python
from abc import ABC, abstractmethod

class IReadable(ABC):
    @abstractmethod
    def read(self):
        pass

class IWritable(ABC):
    @abstractmethod
    def write(self, data):
        pass

class FileManager(IReadable, IWritable):
    def read(self):
        return "Reading data"

    def write(self, data):
        print("Writing:", data)
```
---

# 1. Abstract Properties

## What they are

An **abstract property** is a property in an abstract base class that must be implemented in any subclass.
This allows you to enforce that certain attributes exist and are exposed as properties (not regular methods).

## When to use

* When you want every subclass to define a required attribute in a clean, property-like manner.
* When the value should be computed or protected using getter/setter logic.
* Useful in frameworks, ORMs, or APIs where objects must expose standardized attributes.

## Example

```python
from abc import ABC, abstractmethod

class Employee(ABC):

    @property
    @abstractmethod
    def salary(self):
        pass

class FullTimeEmployee(Employee):

    @property
    def salary(self):
        return 50000

class ContractEmployee(Employee):

    @property
    def salary(self):
        return 30000

e = FullTimeEmployee()
print(e.salary)
```

## Use case example

Imagine an HR system where all employee types must expose a salary value.
Using an abstract property ensures every subclass provides it.

---

# 2. Abstract Class Methods

## What they are

An **abstract class method** is a method that must be overridden in subclasses but is called on the class, not on an object.
It uses both `@classmethod` and `@abstractmethod`.

## When to use

* When subclasses should provide class-level configuration.
* When the method should operate on the class rather than specific instances.
* Example: loading handlers, factory methods, or plugin systems.

## Example

```python
from abc import ABC, abstractmethod

class DataLoader(ABC):

    @classmethod
    @abstractmethod
    def load(cls):
        pass

class JSONLoader(DataLoader):

    @classmethod
    def load(cls):
        return {"status": "json loaded"}

class CSVLoader(DataLoader):

    @classmethod
    def load(cls):
        return ["row1", "row2"]

print(JSONLoader.load())
```

## Use case example

Suppose your system supports different file formats.
Each loader class must define how it loads its data, but the method should belong to the class itself (not an instance).
This is common in serialization, factory patterns, and plugin discovery.

---

# 3. Abstract Static Methods

## What they are

An **abstract static method** is a method that must be overridden in subclasses but does not take a `self` or `cls` argument.
It behaves like a normal function inside the class.

## When to use

* When the method should not depend on class or instance state.
* When you need utility functions that must exist in all subclasses.
* Useful for validation, transformations, conversions, or format checking.

## Example

```python
from abc import ABC, abstractmethod

class Validator(ABC):

    @staticmethod
    @abstractmethod
    def is_valid(value):
        pass

class NumberValidator(Validator):

    @staticmethod
    def is_valid(value):
        return isinstance(value, (int, float)) and value >= 0

class StringValidator(Validator):

    @staticmethod
    def is_valid(value):
        return isinstance(value, str) and len(value) > 0

print(NumberValidator.is_valid(10))
print(StringValidator.is_valid("hello"))
```

## Use case example

In form validation systems or data processing pipelines, every validator must define how it checks validity.
The method does not depend on object or class state, making static methods appropriate.

---
