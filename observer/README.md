This is a foundational pattern for modern application development. If you have ever used a "Subscribe" button or written an event handler in a UI framework (like JavaScript `addEventListener`), you have used the Observer pattern.

### **Pattern \#5: The Observer Pattern**

The Observer is a **Behavioral Pattern**. It focuses on communication between objects.

#### **The Core Concept**

The Observer pattern defines a one-to-many dependency between objects. When one object (the **Subject** or **Publisher**) changes its state, all its dependents (the **Observers** or **Subscribers**) are notified and updated automatically.

Think of it like a **YouTube Channel**.

  * The YouTuber is the **Subject**.
  * The Viewers are the **Observers**.
  * When a new video is uploaded, the YouTuber doesn't call every viewer personally. They just hit "Upload," and YouTube notifies everyone who hit the "Subscribe" bell.

#### **Scenario & Situation**

You apply this when a change to one object requires changing others, and you don't know how many objects need to be changed or who they are.

**Common Scenarios:**

1.  **Stock Market App:** The stock price (Subject) changes. The UI chart, the user's portfolio balance, and the database history (Observers) all need to update instantly.
2.  **Chat Applications:** When a new message arrives in a room, all connected clients need to display it.
3.  **Newsletters:** A blog publishes a post, and emails are sent to thousands of subscribers.

#### **What Goes Wrong If NOT Used?**

If you don't use the Observer pattern, you usually fall into the trap of **Polling** or **Tight Coupling**.

  * **The Polling Problem (The "Are we there yet?" Loop):** Without Observer, the UI has to constantly ask the database: "Do you have new data? How about now? Now?" This wastes massive amounts of CPU and network resources.
  * **The Coupling Problem:** The Stock Price class would need code like:
    ```python
    def update_price(self, new_price):
        self.price = new_price
        # Hard dependency on specific classes
        ui_screen.repaint()
        database.save()
        logger.log()
    ```
    If you want to add a Mobile App notification later, you have to modify the Stock Price class code. That is bad design.

-----

#### **Python Implementation**

Let's build a **Weather Station** system. The station reads the temperature, and multiple display screens (Phone, Window, Logger) update automatically.

```python
from abc import ABC, abstractmethod

# 1. The Observer Interface
# All subscribers must implement this so the Subject knows how to talk to them.
class Observer(ABC):
    @abstractmethod
    def update(self, temperature):
        pass

# 2. The Subject (Publisher)
# This manages the list of subscribers and notifies them.
class WeatherStation:
    def __init__(self):
        self._observers = []  # List to hold subscribers
        self._temperature = 0

    def attach(self, observer: Observer):
        print(f"Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def set_temperature(self, temp):
        print(f"\nSubject: New temperature measurement: {temp}C")
        self._temperature = temp
        self._notify()

    def _notify(self):
        print("Subject: Notifying observers...")
        for observer in self._observers:
            # The Subject doesn't care WHO the observer is, 
            # only that it has an .update() method.
            observer.update(self._temperature)

# 3. Concrete Observers
class PhoneDisplay(Observer):
    def update(self, temperature):
        print(f"  -> Phone Display: Current temp is {temperature}C")

class WindowDisplay(Observer):
    def update(self, temperature):
        print(f"  -> Window Display: Reacting to {temperature}C")

# --- Client Code ---

station = WeatherStation()

phone = PhoneDisplay()
window = WindowDisplay()

# 1. Register the observers
station.attach(phone)
station.attach(window)

# 2. Change state (simulates a sensor reading)
station.set_temperature(25)

# 3. Dynamic behavior: Remove one observer and update again
station.detach(phone)
station.set_temperature(30)
```

**Output Analysis:**

1.  When temp changes to 25, **both** Phone and Window print their updates.
2.  We detach the Phone.
3.  When temp changes to 30, **only** the Window updates.
4.  The `WeatherStation` never needed to know exactly what a `PhoneDisplay` is; it only knew it was an `Observer`.

#### **Perks of the Observer Pattern**

  * **Open/Closed Principle:** You can introduce new subscriber classes (e.g., `ThermostatController`) without changing the publisher's code.
  * **Establish Relations at Runtime:** You can subscribe and unsubscribe objects dynamically (like a user turning notifications on/off in settings).
  * **Push vs Pull:** The data is pushed to the consumer the moment it is available, rather than the consumer checking constantly.

-----
