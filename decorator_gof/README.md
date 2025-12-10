
### **Pattern \#4: The Decorator Pattern**
This is a crucial pattern for Python developers. While many languages use this pattern, Python has baked it directly into the syntax of the language.

The Decorator is a **Structural Pattern**. Unlike Creational patterns (which build objects) or Behavioral patterns (which run logic), Structural patterns deal with how classes and objects are composed to form larger structures.

#### **The Core Concept**

The Decorator allows you to attach new behaviors to objects dynamically by placing these objects inside special wrapper objects that contain the behaviors.

Think of it like **Wearing Layers of Clothing**.

  * You (the Object) start cold.
  * You put on a sweater (Decorator 1). You are now "You + Warmth".
  * You put on a raincoat (Decorator 2). You are now "You + Warmth + Dry".
  * You are still "You", but your behavior (handling cold/rain) has changed based on what you are wrapped in.

#### **Scenario & Situation**

You apply this when you want to add functionality to an object *without* altering its structure or creating a crazy inheritance tree.

**Common Scenarios:**

1.  **Data Processing:** You write data to a file. Sometimes you want it compressed. Sometimes encrypted. Sometimes both.
2.  **Web Frameworks (Flask/Django):** You have a function that returns a webpage. You want to "wrap" it so that only logged-in users can see it (Authentication Decorator).
3.  **UI Components:** You have a window. You want to add a scrollbar, then a border, then a shadow.

#### **What Goes Wrong If NOT Used?**

If you rely on Inheritance instead of Decorators, you get the **Class Explosion** problem.

Imagine a `FileStream` class.

  * You need encryption? -\> `EncryptedFileStream`.
  * You need compression? -\> `CompressedFileStream`.
  * You need both? -\> `EncryptedCompressedFileStream`.
  * You need to add buffering? -\> `BufferedEncryptedCompressedFileStream`...

This is unmaintainable. Decorators let you mix and match at runtime.

-----

#### **Python Implementation**

In Python, we have two ways to do this. I will show you the **Classic OOP approach** (Classes) first, as this explains the design structure. Then I will show you the **Pythonic Syntax** (`@`), which is what you'll use daily.

**1. The Classic OOP Approach (The Wrapper)**

Let's build a text processor.

```python
from abc import ABC, abstractmethod

class TextPublisher(ABC):
    @abstractmethod
    def publish(self) -> str:
        pass

class SimpleText(TextPublisher):
    def __init__(self, text: str):
        self._text = text

    def publish(self) -> str:
        return self._text

class TextDecorator(TextPublisher):
    def __init__(self, component: TextPublisher):
        self._component = component

    def publish(self) -> str:
        return self._component.publish()

class HTMLDecorator(TextDecorator):
    def publish(self) -> str:
        return f"<html>{super().publish()}</html>"

class UpperCaseDecorator(TextDecorator):
    def publish(self) -> str:
        return super().publish().upper()


msg = SimpleText("hello world")
html_msg = HTMLDecorator(msg)
fancy_msg = UpperCaseDecorator(html_msg)

print(fancy_msg.publish())
```

**2. The Pythonic Syntax (Syntactic Sugar)**
Python simplifies the above pattern for functions using the `@` symbol. This is what you see in Flask or fastAPI.

```python
# A function decorator
def make_bold(func):
    def wrapper():
        return "<b>" + func() + "</b>"
    return wrapper

def make_italic(func):
    def wrapper():
        return "<i>" + func() + "</i>"
    return wrapper

# Using the decorators
@make_bold
@make_italic
def say_hello():
    return "Hello Python"

# This is equivalent to: make_bold(make_italic(say_hello))
print(say_hello()) 
# Output: <b><i>Hello Python</i></b>
```

#### **Perks of the Decorator Pattern**

  * **Recursive Composition:** You can wrap an object infinitely (e.g., wrap a gift, then wrap that box, then put it in a bag).
  * **Runtime Modification:** You don't need to define `HTMLUpperCaseText` as a class. You just compose it when the program runs.
  * **Single Responsibility:** You split "HTML formatting" and "Uppercasing" into tiny, manageable classes.

-----