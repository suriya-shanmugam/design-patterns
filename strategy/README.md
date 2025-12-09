**Behavioral Pattern** is one of the most useful patterns in software engineering because it helps you follow the Golden Rule of OOP: *Favor Composition over Inheritance.*

### **Pattern \#3: The Strategy Pattern**

[Image of Strategy pattern UML class diagram]

While the Factory pattern helps you *create* different objects, the Strategy pattern helps you *change what an object does* dynamically.

#### **The Core Concept**

The Strategy pattern allows you to define a family of algorithms, put each of them in a separate class, and make their objects interchangeable.

Think of it like a **Game Console**. The console (Context) is the same box, but inserting a different cartridge (Strategy) changes the game entirely.

#### **Scenario & Situation**

You apply this when you have multiple ways to do a specific task, and you need to switch between them at runtime.

**Common Scenarios:**

1.  **Navigation Apps:** You need to calculate a route from A to B. The logic differs if the user selects "Walking," "Driving," or "Public Transport."
2.  **Sorting Data:** You might use QuickSort for large datasets but MergeSort for smaller ones.
3.  **Discounts/Pricing:** A shopping cart might apply different pricing logic based on whether the user is a "VIP," "Regular," or has a "Holiday Coupon."

#### **What Goes Wrong If NOT Used?**

If you don't use Strategy, you create the **"Giant If-Else" Monster**.

  * **The Complexity Problem:** You end up with a single class containing a massive method with endless `if type == 'car': ... elif type == 'walk': ...`.
  * **The Maintenance Nightmare:** If you need to fix a bug in the "Walking" logic, you have to open the file that also contains the "Driving" logic, risking bugs in unrelated features.

-----

#### **Python Implementation**

Let's build a **Navigation Route Builder**. We want to calculate a route, but the algorithm changes based on travel mode.

```python
from abc import ABC, abstractmethod
from typing import List

# 1. The Strategy Interface
# Defines the common method all strategies must have.
class RouteStrategy(ABC):
    @abstractmethod
    def build_route(self, a: str, b: str) -> str:
        pass

# 2. Concrete Strategies
# The specific algorithms.
class RoadStrategy(RouteStrategy):
    def build_route(self, a: str, b: str) -> str:
        return f"Road Route from {a} to {b}: Drive on I-95, takes 30 mins."

class WalkingStrategy(RouteStrategy):
    def build_route(self, a: str, b: str) -> str:
        return f"Walking Route from {a} to {b}: Walk through the park, takes 2 hours."

class TransitStrategy(RouteStrategy):
    def build_route(self, a: str, b: str) -> str:
        return f"Transit Route from {a} to {b}: Take Bus #42, takes 45 mins."

# 3. The Context
# This is the main application object. It holds a reference to a Strategy.
class Navigator:
    def __init__(self, strategy: RouteStrategy):
        self._strategy = strategy

    # This allows us to swap the 'cartridge' at runtime
    def set_strategy(self, strategy: RouteStrategy):
        print(f"--- Switching Mode to {type(strategy).__name__} ---")
        self._strategy = strategy

    def get_directions(self, a, b):
        # Delegate the work to the strategy object
        result = self._strategy.build_route(a, b)
        print(result)

# --- Client Code ---

# Default to Road
nav = Navigator(RoadStrategy())
nav.get_directions("Home", "Office")

# User clicks "Walk" button -> We swap the strategy dynamically
nav.set_strategy(WalkingStrategy())
nav.get_directions("Home", "Office")

# User clicks "Bus" button
nav.set_strategy(TransitStrategy())
nav.get_directions("Home", "Office")
```

**Output Analysis:**

1.  Notice that the `Navigator` class is very clean. It doesn't know *how* to calculate a route; it just asks the strategy to do it.
2.  We switched behavior three times without ever creating a new `Navigator` object. We just changed its internal "brain" (the strategy).

#### **Perks of the Strategy Pattern**

  * **Open/Closed Principle:** You can add a new strategy (e.g., `BikeStrategy`) without changing the `Navigator` code.
  * **Runtime Flexibility:** You can swap algorithms on the fly based on user interaction.
  * **Testability:** You can test the `RoadStrategy` in isolation without worrying about the rest of the navigation app.

-----