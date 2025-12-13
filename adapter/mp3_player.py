from media_player_base import MediaPlayer 

class Mp3Player(MediaPlayer):
    def play(self, filename):
        print(f"[Mp3Player] Playing the song {filename}")
