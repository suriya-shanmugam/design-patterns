This is the ultimate "integration" pattern. You will use this often when connecting your clean code to messy legacy systems or third-party libraries that you cannot control.

### **Pattern \#6: The Adapter Pattern**

The Adapter is a **Structural Pattern**. It acts as a bridge between two incompatible interfaces.

#### **The Core Concept**

The Adapter pattern allows objects with incompatible interfaces to collaborate. It wraps an existing object (the **Adaptee**) and exposes a standard interface (the **Target**) that your client code understands.

Think of it literally like a **Power Adapter**.

  * Your laptop plug (Client) has 3 prongs.
  * The wall socket (Adaptee) has 2 holes.
  * They cannot talk directly. You need an adapter that accepts the 3 prongs on one side and fits into the 2 holes on the other. The adapter translates the connection.

#### **Scenario & Situation**

You apply this when you want to use an existing class, but its interface doesn't match the one you need.

**Common Scenarios:**

1.  **Legacy Code:** You are replacing an old library (e.g., an old XML parser) with a new modern one (a JSON parser), but you don't want to rewrite your entire application to match the new library's method names.
2.  **Third-Party APIs:** You are integrating a payment provider. Your app expects `pay(amount)`, but the external library requires `make_payment(dollars, cents)`.
3.  **Data Format Conversion:** Your system expects data in Imperial units, but a new sensor you bought only outputs Metric.

#### **What Goes Wrong If NOT Used?**

If you don't use an Adapter, you end up with **Invading Dependencies**.

  * **The "Spaghetti" Problem:** You pollute your clean business logic with specific calls to the external library.
      * Instead of `payment.process()`, you have `if provider == 'stripe': stripe.charge_card() elif provider == 'paypal': paypal.send_money()`.
  * **The "Vendor Lock-in" Problem:** If the third-party library changes its method names in version 2.0, you have to find and fix every single place you called it in your entire application. With an adapter, you only fix it in *one* place (the adapter class).

-----

#### **Python Implementation**

Let's imagine your app is built to work with a `MediaPlayer` that plays MP3s. Suddenly, you need to support a new fancy audio format called "VLC", but the VLC library has completely different method names.

```python
from abc import ABC, abstractmethod

# 1. Target interface
# What the app / client is coded against.
class MediaPlayer(ABC):
    @abstractmethod
    def play(self, filename: str) -> None:
        pass


# 2. Existing concrete implementation that already works with the client
class MP3Player(MediaPlayer):
    def play(self, filename: str) -> None:
        print(f"[MP3Player] Playing MP3 file: {filename}")


# 3. The Adaptee (3rd-party / legacy class you can't change)
class VLCPlayer:
    def heavy_vlc_play(self, source_path: str, speed: float, normalize: bool) -> None:
        print(
            f"[VLCPlayer] Playing '{source_path}' at {speed}x speed "
            f"{'(normalized)' if normalize else ''}"
        )


# 4. The Adapter: makes VLCPlayer look like a MediaPlayer
class VLCAdapter(MediaPlayer):
    def __init__(self, vlc_player: VLCPlayer, default_speed: float = 1.0) -> None:
        self._vlc_player = vlc_player
        self._default_speed = default_speed

    def play(self, filename: str) -> None:
        # Translate the simple 'play(filename)' call into the more complex VLC call
        print("[VLCAdapter] Adapting 'play' to 'heavy_vlc_play'...")
        self._vlc_player.heavy_vlc_play(
            source_path=filename,
            speed=self._default_speed,
            normalize=True,   # reasonable default
        )


# --- Client code ---

def run_music_app(player: MediaPlayer, song: str) -> None:
    # The client only knows about MediaPlayer.
    player.play(song)


if __name__ == "__main__":
    # Scenario A: using the existing MP3 player
    mp3_player = MP3Player()
    run_music_app(mp3_player, "song.mp3")

    print("-" * 20)

    # Scenario B: using an incompatible VLC library via Adapter
    vlc = VLCPlayer()
    vlc_player_adapter = VLCAdapter(vlc, default_speed=1.25)
    run_music_app(vlc_player_adapter, "movie.mkv")

```

**Output Analysis:**

1.  The first call works normally (`Playing MP3...`).
2.  The second call goes through the Adapter. The client calls `play`, but the Adapter translates that into `heavy_vlc_play`.
3.  The client code (`run_music_app`) never had to change to support the new format.

#### **Perks of the Adapter Pattern**

  * **Single Responsibility Principle:** You separate the interface conversion code from the primary business logic.
  * **Open/Closed Principle:** You can introduce new types of adapters (e.g., `SpotifyAdapter`) into the program without breaking the existing client code.
  * **Reusability:** You can reuse the weird third-party class without modifying it (which you often can't do anyway because it's a library).

-----