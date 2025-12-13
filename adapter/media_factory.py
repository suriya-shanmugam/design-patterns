from media_player_base import MediaPlayer
from mp3_player import Mp3Player
from vlc_adapter import VLCAdapter
from vlc_player import VLCPlayer

def create_media_player() -> MediaPlayer:
    # this could be based on config/env flags
    use_vlc = True

    if use_vlc:
        return VLCAdapter(VLCPlayer(), speed=1.0)
    else:
        return Mp3Player()

