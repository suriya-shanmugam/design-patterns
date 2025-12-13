from media_player_base import MediaPlayer 
from vlc_player import VLCPlayer

class VLCAdapter(MediaPlayer):
    def __init__(self, vlc_player:VLCPlayer, speed:float=1.0):
        self._vlc_player = vlc_player
        self._speed = speed

    def play(self, file_name):
        print(f"[VLCAdapter] Adapting [play()] to [heavy_play()]")
        self._vlc_player.heavy_play(file_name, self._speed, normalize=True)
