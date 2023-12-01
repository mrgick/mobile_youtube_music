from kivy.lang import Builder
from kivy.uix.screenmanager import NoTransition, ScreenManager
from kivymd.app import MDApp

from screens.player_screen import PlayerScreen
from screens.playlists_screen import PlaylistsScreen
from screens.search_screen import SearchScreen
from pathlib import Path

from kivy.core.window import Window
Window.size = (400, 800)

class YoutubeMusicApp(MDApp):
    dialog = None

    def build(self):
        self.music_path = Path('music')
        screens = Path('screens')
        Builder.load_file("main.kv")
        Builder.load_file(str(screens / "search_screen.kv"))
        Builder.load_file(str(screens / "playlists_screen.kv"))
        Builder.load_file(str(screens / "player_screen.kv"))
        # Builder.load_file(str(screens / "playlists_screen.kv"))
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(SearchScreen(name="search_screen"))
        sm.add_widget(PlaylistsScreen(name="playlists_screen"))
        sm.add_widget(PlayerScreen(name="player_screen"))
        self.sm = sm
        return sm

    def switch_screen(self, screen_name: str):
        self.sm.current = screen_name


if __name__ == "__main__":
    YoutubeMusicApp().run()
