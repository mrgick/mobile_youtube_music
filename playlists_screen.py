from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, ThreeLineAvatarListItem
from pathlib import Path

MUSIC_DIR = Path('music')

def get_playlists() -> list[Path]:
    return [x for x in MUSIC_DIR.iterdir() if x.is_dir()]

class PlaylistsScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        playlists = get_playlists()
        print(playlists)
