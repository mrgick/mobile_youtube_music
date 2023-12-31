from pathlib import Path

# from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import NoTransition, ScreenManager
from kivy.utils import platform
from kivymd.app import MDApp

from screens.player_screen import PlayerScreen
from screens.playlist_detail_screen import PlaylistDetailScreen
from screens.playlists_screen import PlaylistsScreen
from screens.search_screen import SearchScreen
from screens.settings_screen import SettingsScreen

# Window.size = (400, 800)


class YoutubeMusicApp(MDApp):
    dialog = None

    def build(self):
        self.music_path = None
        self.playlist_path = None
        screens = Path("screens")
        Builder.load_file("main.kv")
        Builder.load_file(str(screens / "search_screen.kv"))
        Builder.load_file(str(screens / "playlists_screen.kv"))
        Builder.load_file(str(screens / "player_screen.kv"))
        Builder.load_file(str(screens / "playlist_detail_screen.kv"))
        Builder.load_file(str(screens / "settings_screen.kv"))
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Light"
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(SearchScreen(name="search_screen"))
        sm.add_widget(PlaylistDetailScreen(name="playlist_detail_screen"))
        sm.add_widget(PlaylistsScreen(name="playlists_screen"))
        sm.add_widget(PlayerScreen(name="player_screen"))
        sm.add_widget(SettingsScreen(name="settings_screen"))
        self.sm = sm
        return sm

    def on_start(self):
        self.set_music_path(Path("music"))

    def set_music_path(self, path):
        if platform == "android":
            from android.permissions import request_permissions, check_permission, Permission
            request_permissions([Permission.INTERNET, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            from android.storage import app_storage_path # https://github.com/Android-for-Python/Android-for-Python-Users/blob/main/README.md#app-storage-directory
            _path = Path(app_storage_path())
            _path = _path / "cache"
            _path.mkdir(exist_ok=True)
            self.music_path = _path
        else:
            self.music_path = Path("music")
            self.music_path.mkdir(exist_ok=True)

    def switch_screen(self, screen_name: str):
        self.sm.current = screen_name

    def switch_theme(self, value):
        self.theme_cls.theme_style = "Dark" if value else "Light"
        self.theme_cls.primary_palette = "Blue" if value else "Orange"


if __name__ == "__main__":
    YoutubeMusicApp().run()
