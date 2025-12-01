### **The Singleton Pattern**

We are starting here because almost every application needs a "single source of truth." The Singleton is a **Creational Pattern**.

#### **The Core Concept**

The Singleton pattern ensures that a class has **only one instance** and provides a global point of access to that instance. No matter how many times you try to initialize the class, you get back the exact same object.

#### **Scenario & Situation**

You apply this pattern when multiple parts of your application need to share the exact same resource or state.

**Common Scenarios:**

1.  **Database Connections:** Creating a new connection for every query is expensive and can crash the database. You want one shared connection pool.
2.  **Configuration Settings:** If your app loads `config.json` at startup, you don't want to reload that file every time a function needs to check a setting. You want one object holding that config in memory.
3.  **Logging:** You want all parts of your app writing to the same log file in a synchronized way.

#### **What Goes Wrong If NOT Used?**

If you *don't* use a Singleton in these scenarios, you risk **State Inconsistency** and **Resource Exhaustion**.

  * **The "Split Brain" Problem:** Imagine you have a `GameSettings` class. If Player A changes the volume, but Player B's screen creates a *new* instance of `GameSettings`, Player B won't see the volume change. They are looking at two different objects.
  * **The "Crash" Problem:** If 1,000 users hit your API and you open 1,000 separate database connections (instead of reusing one), your database will likely run out of memory and crash.

-----

#### **Python Implementation**

In Python, we override the `__new__` method. While `__init__` initializes an object, `__new__` is the method that actually *creates* it. By intercepting this, we can check if an instance already exists.

```python
class DatabaseConnection:
    _instance = None  # Class-level variable to store the single instance

    def __new__(cls):
        # If the instance doesn't exist yet, create it.
        if cls._instance is None:
            print("Creating the Database Connection...")
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            # Initialize the connection logic here (e.g., connect to DB)
            cls._instance.connection_status = "Connected"
        return cls._instance

    def query(self, sql):
        print(f"Executing {sql} on connection: {id(self)}")

# --- Client Code ---

# Let's try to create two different instances
db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(f"db1 ID: {id(db1)}")
print(f"db2 ID: {id(db2)}")

# Proof they are the same
print(f"Are they the same object? {db1 is db2}")

# Both use the same state
db1.query("SELECT * FROM users")
db2.query("SELECT * FROM orders")
```

**Output Analysis:**

1.  You will see "Creating the Database Connection..." print only **once**.
2.  The `id(db1)` and `id(db2)` will be identical numbers (memory addresses).
3.  `db1 is db2` will return `True`.

#### **Perks of the Singleton**

  * **Controlled Access:** You have strict control over how and when the global instance is accessed.
  * **Memory Efficiency:** You avoid allocating memory for unnecessary duplicate objects.
  * **Lazy Initialization:** You can delay the creation of the object until the very moment it is first needed (useful if the object is heavy, like a DB connection).

-----
# Object creation Flow
---

#  **1. How Python Allocates and Initializes Objects: `__new__` vs `__init__`**

In Python, object creation happens in **two steps**:

## **Step 1 — Allocation: `__new__`**

* `__new__` is a **static method** (even if defined inside a class) responsible for:

  * Allocating memory for a new instance
  * Returning the new object

* It is called **before** `__init__`

* Its signature is typically:

  ```python
  def __new__(cls, *args, **kwargs):
      # allocate object
      return super().__new__(cls)
  ```

### Key Properties of `__new__`:

* Must **return an object** (usually an instance of `cls`)
* If it returns an instance of a *different* class, `__init__` of the original class is **skipped**
* Used for:

  * Immutable types (`int`, `str`, `tuple`)
  * Controlling instance creation (Singleton, Flyweight, caching)

---

## **Step 2 — Initialization: `__init__`**

* `__init__` initializes the **already created instance**
* It does **not** return anything (should return `None`)
* It is called immediately after `__new__` returns an instance

### Key Properties of `__init__`:

* Used to configure instance attributes
* Cannot prevent object creation—only configures the instance already created in `__new__`

---

## **Flow Summary**

```
obj = MyClass(arg1, arg2)

Python internally does:
instance = MyClass.__new__(MyClass, arg1, arg2)
if isinstance(instance, MyClass):
    MyClass.__init__(instance, arg1, arg2)
return instance
```

---

# **2. Subclass Override Behavior**

Subclassing affects both `__new__` and `__init__`:

## **If subclass overrides `__init__`**

* It must call `super().__init__()` explicitly if the parent initialization is required.
* If not called, the parent `__init__` is skipped.

```python
class A:
    def __init__(self):
        print("A init")

class B(A):
    def __init__(self):
        print("B init")
        super().__init__()
```

## **If subclass overrides `__new__`**

Same concept: call `super().__new__(cls)` to actually allocate memory.

```python
class B(A):
    def __new__(cls):
        print("B new")
        return super().__new__(cls)
```

If `__new__` does *not* return an instance of `cls`, then `__init__` will not run:

```python
class A:
    def __new__(cls):
        print("__new__")
        return 42   # not instance of A

    def __init__(self):
        print("__init__")  # never called
```

---

# **3. `__new__` as a static method of a class**

Although defined inside the class, `__new__` is technically a **static method** because:

* It receives the class (`cls`) explicitly as the first argument
* It is called before the instance exists
* It does not get a `self`
* Python automatically treats it like:

  ```python
  __new__ = staticmethod(__new__)
  ```

Example:

```python
class A:
    def __new__(cls, *args, **kwargs):
        print("Allocating", cls)
        obj = super().__new__(cls)
        return obj
```

---

# **Putting it Together: Object Flow**

Here’s the complete lifecycle:

```
call ClassName(...)
    ↓
ClassName.__new__(cls, ...)
    ↳ allocates memory for object
    ↳ returns instance
    ↓
ClassName.__init__(self, ...)
    ↳ initializes attributes
```

---

# **4. Using `__new__` to Build a Singleton**

Singleton: **only one instance of a class exists**.

Since `__new__` controls allocation, we override it:

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Creating the instance")
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        self.value = value
```

Usage:

```python
a = Singleton(1)
b = Singleton(2)
print(a.value, b.value)  # both 2 — same instance
print(a is b)            # True
```

Why `__new__` works for this?

* Because `__init__` cannot control allocation or return a different instance.
* Only `__new__` decides whether to create or reuse an object.

---

# **Key Takeaways**

| Concept           | Role                                                          |
| ----------------- | ------------------------------------------------------------- |
| `__new__`         | Allocates memory, returns object (static method)              |
| `__init__`        | Initializes the object (instance method)                      |
| Subclass override | Must call `super()` manually for both methods                 |
| Singleton         | Implemented via `__new__` because it controls object creation |

---
