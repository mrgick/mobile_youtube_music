from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import (
    ThreeLineAvatarIconListItem,
    MDList,
    ImageLeftWidgetWithoutTouch,
)
from kivy.lang import Builder
from ytmusicapi import YTMusic
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import BoxLayout
from search_screen import SearchScreen
from playlists_screen import PlaylistsScreen
from player_screen import PlayerScreen

from kivy.uix.screenmanager import ScreenManager, NoTransition






class YoutubeMusicApp(MDApp):
    dialog = None
    def build(self):
        Builder.load_file("main.kv")
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(SearchScreen(name="search_screen"))
        sm.add_widget(PlaylistsScreen(name="playlists_screen"))
        sm.add_widget(PlayerScreen(name="player_screen"))
        self.sm = sm
        return sm

    def switch_screen(self, screen_name:str):
        self.sm.current = screen_name


if __name__ == "__main__":
    YoutubeMusicApp().run()
