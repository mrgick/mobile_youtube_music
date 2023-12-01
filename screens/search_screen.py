import threading
from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import (
    ThreeLineAvatarListItem,
    MDList,
    ImageLeftWidgetWithoutTouch,
)
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from .playlists_screen import get_playlists
from kivymd.uix.list import MDList, OneLineListItem
from pathlib import Path
from utils.yt_api import search_music, download_music, add_metadata
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.label import MDLabel
from kivy.clock import Clock

class SongDialog(MDBoxLayout):
    def __init__(self, song, **kwargs):
        super().__init__(**kwargs)
        self.song = song
        mdlist: MDList = self.ids.playlists_list
        mdlist.clear_widgets()
        for x in get_playlists():
            item = OneLineListItem(
                text=str(x.name), on_release=lambda y: self.download_file(x)  # noqa: B023
            )
            mdlist.add_widget(item)

    def download_file(self, dir_path: Path):
        self.download_text = ''
        self.download_complete = False
        Clock.schedule_interval(self.show_spinner, 1)
        download_thread = threading.Thread(target=self.download_music_thread, args=(dir_path,))
        download_thread.start()

    def show_spinner(self, dt):
        self.clear_widgets()
        spinner = MDSpinner(size_hint=(None, None), size=(48, 48), pos_hint={'center_x': .5, 'center_y': .5})
        self.add_widget(spinner)
        if self.download_text:
            self.add_widget(MDLabel(text=self.download_text, pos_hint={'center_x': .5, 'center_y': .5}))
        if self.download_complete:
            self.clear_widgets()
            self.add_widget(MDLabel(text="Download complete", pos_hint={'center_x': .5, 'center_y': .5}))

    def download_music_thread(self, dir_path):
        download_music(self.song, dir_path, lambda x: self.update_status(x))
        self.download_text = "Adding metadata to file"
        add_metadata(self.song, dir_path)
        self.download_complete = True

    def update_status(self, x):
        if x and x.get('speed') and x.get('_percent_str'):
            self.download_text = f"Downloading: {x['speed']/1048576:.2f}Mb, {x['_percent_str'].split('m')[1].split('%')[0]}%"

class SearchScreen(MDScreen):
    def search_music(self, search_text: str):
        videos_list: MDList = self.ids.videos_list
        videos_list.clear_widgets()
        for song in search_music(search_text):
            third_str = ""
            if song["year"]:
                third_str = f'Year: {song["year"]},  '
            if song["artists"]:
                artists = ", ".join(x["name"] for x in song["artists"])
                third_str = f"{third_str}Artists: {artists},  "
            if song['album']:
                third_str = f"{third_str}Album: {song['album']['name']}"
            item = ThreeLineAvatarListItem(
                text=song["title"],
                secondary_text=f'Duration: {song["duration"]}',
                tertiary_text=third_str,
                on_release=self.open_song_dialog,
            )
            item.details = song
            item.add_widget(
                ImageLeftWidgetWithoutTouch(source=song["thumbnails"][-1]["url"])
            )
            videos_list.add_widget(item)

    def open_song_dialog(self, item):
        song = item.details
        app = MDApp.get_running_app()
        app.dialog = MDDialog(
            title=f'Add \"{song["title"]}\" to playlist:',
            type="custom",
            content_cls=SongDialog(song),
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: app.dialog.dismiss(),
                ),
            ],
        )
        app.dialog.open()
