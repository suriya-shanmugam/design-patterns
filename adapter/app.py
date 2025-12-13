from media_player_base import MediaPlayer 
from media_factory import create_media_player

def run_music_app(player:MediaPlayer, song_path:str):
    player.play(song_path)

if __name__ == '__main__':
    
    player = create_media_player()
    run_music_app(player, "let_it_be.mp3")

