#  1. What Is a Decorator in Python?

A **decorator** is simply:

> **A function that takes another function (or class) and returns a modified or enhanced version of it.**

It is built on Python’s first-class functions and higher-order functions.

### Basic form:

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        # extra behavior
        return func(*args, **kwargs)
    return wrapper
```

Then applied as:

```python
@decorator
def some_function():
    pass
```

The `@decorator` syntax is just syntactic sugar for:

```python
some_function = decorator(some_function)
```

---

#  2. How Decorators Work Internally

Decorators rely on 2 key Python features:

### **1. Functions are first-class objects**

You can pass functions as arguments, return them from functions, store them in variables, etc.

### **2. Closures**

The inner `wrapper` function remembers the environment (the wrapped function) even after the decorator finishes executing.

---

# 3. Why Decorators Are Useful

Decorators allow you to insert behavior *around* an existing function without modifying that function directly.

Common uses:

* Logging
* Authentication & permission checks
* Caching / memoization
* Performance timing
* Transaction management
* Retry logic
* Rate limiting
* API routing
* Registration of plugins / commands

---

#  4. Function Decorator — Simple Example

### Basic logging decorator:

```python
def log(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log
def greet():
    print("Hello")
```

Output:

```
Calling greet
Hello
```

---

#  5. Decorator with Arguments

Sometimes you want the decorator itself to take parameters:

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("Hi!")
```

---

#  6. Preserving Function Metadata with `functools.wraps`

Without `wraps`, decorators break metadata:

```python
greet.__name__  # becomes 'wrapper'
```

Solution:

```python
from functools import wraps

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Log")
        return func(*args, **kwargs)
    return wrapper
```

Now metadata is preserved.

---

#  7. Decorating Classes (Class Decorators)

Decorators can also enhance classes:

```python
def register(cls):
    registry[cls.__name__] = cls
    return cls

@register
class Service:
    pass
```

---

#  8. Using Classes as Decorators

A class with `__call__` can be used as a decorator:

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

@CountCalls
def hello():
    print("hello")
```

---

#  9. Decorators in Python Frameworks (Where You See Them Everywhere)

### **Flask / FastAPI — Routing**

```python
@app.get("/users")
def list_users():
    return ...
```

### **Django — Permissions**

```python
@login_required
def dashboard(request):
    ...
```

### **pytest — Markers**

```python
@pytest.mark.parametrize("x", [1,2,3])
def test_add(x):
    ...
```

### **Celery — Tasks**

```python
@app.task
def process_image():
    ...
```

### **Typer / Click — CLI commands**

```python
@app.command()
def run():
    ...
```

Why decorators are so common in frameworks:

* They allow **declarative programming** (clean, readable, metadata-based code)
* They let frameworks **register functions automatically**
* They keep code **cleaner than manual registration**
* They add behaviors **without altering the function body**

---

#  10. Decorator Chain (Stacking Decorators)

Decorators can be stacked:

```python
@auth_required
@log
@cache
def get_data():
    ...
```

Order of execution:

```
get_data = auth_required(log(cache(get_data)))
```

---

#  11. Advanced Patterns

### **1. Decorators for caching**

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def compute(x):
    return x * x
```

### **2. Decorators for context management**

```python
@contextmanager
def file_open(path):
    ...
```

### **3. Decorators for dependency injection**

Used in frameworks like FastAPI:

```python
@app.get("/items")
def read(items=Depends(get_items)):
    ...
```

---

#  12. Decorators vs. the GoF “Decorator Pattern”

The Python decorator syntax is NOT the same as the classic OOP pattern.

| Python Decorator              | GoF Decorator Pattern      |
| ----------------------------- | -------------------------- |
| Function wrapper              | Object wrapper             |
| Modify behavior declaratively | Extend behavior at runtime |
| Simple, dynamic               | Heavier, class-based       |

They solve related but not identical problems.

---

#  Summary

Decorators in Python are:

* **Syntactic sugar** for wrapping functions/classes
* **Extremely common** because they support a clean, declarative coding style
* **Heavily used in frameworks** for routing, registration, permissions, dependency injection, and more
* **Powered by closures and first-class functions**
* **Flexible**, supporting arguments, stacking, and class-based implementations

They are one of Python’s most powerful and idiomatic features.

---
#  First: What Is a Closure?

A **closure** in Python is created when:

1. A function (inner function) is defined inside another function.
2. The inner function *uses variables* from the outer function.
3. The outer function returns the inner function.
4. The inner function *remembers* the variables even after the outer function has finished executing.

In simple terms:

> **A closure is a function that carries (“closes over”) the environment in which it was created.**

---

#  Now look at *your code*:

```python
def decorator(func):
    
    def wrapper(*args):
        print("I am a wrapper")
        print(*args)
        return func(*args)
    
    return wrapper
```

When you call:

```python
f1 = decorator(function1)
```

The steps are:

1. `decorator()` receives `func=function1`.
2. It **defines** the inner function `wrapper`, which *uses `func`*.
3. `decorator()` returns `wrapper`.
4. `wrapper` still remembers the value of `func` (which is `function1`).

So `wrapper` is a closure because it **remembers `func`**, even though `decorator()` has already exited.

---

#  Why is this a closure?

Let’s analyze your inner function:

```python
def wrapper(*args):
    print("I am a wrapper")
    print(*args)
    return func(*args)   # <-- this is the key!
```

Inside `wrapper`, you are using the variable `func`.

But `func`:

* is **not a local variable** inside `wrapper`.
* is **not a global variable**.

It comes from the **enclosing function** `decorator`.

Therefore Python marks `wrapper` as a **closure**—a function that “closes over” the variable `func`.

And even after `decorator()` returns, Python keeps `func` alive so that `wrapper` can still call it.

---

#  Visualizing the Closure (Memory Model)

When `f1 = decorator(function1)` runs, Python makes this structure:

```
decorator frame (ends)
│
│  func → function1
│
└── wrapper (closure)
       |
       └── has a pointer to func stored in its __closure__
```

Later, when you call:

```python
f1(1, 2)
```

Even though `decorator()` is long gone, `wrapper` can still access `func` because it's preserved inside the closure.

---

# 🧪 Proof that it is a closure

You can test it:

```python
print(f1.__closure__)
```

You’ll see something like:

```
(<cell at 0x...: function object at 0x...>,)
```

This is Python showing you that `wrapper` *contains a “cell” storing `func`*.

---

#  Summary (easy to memorize)

| Condition for closure                   | In your code                |
| --------------------------------------- | --------------------------- |
| Inner function                          | `wrapper`                   |
| Uses outer variable                     | `func` inside `wrapper`     |
| Outer function returns inner function   | `return wrapper`            |
| Inner function remembers outer variable | `f1 = decorator(function1)` |

Therefore:
**`wrapper` is a closure because it captures (`closes over`) the variable `func` from the outer function.**

---