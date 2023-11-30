from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import (
    ThreeLineAvatarIconListItem,
    MDList,
    ImageLeftWidgetWithoutTouch,
)
from ytmusicapi import YTMusic
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import BoxLayout


class SongDialog(BoxLayout):
    pass


class SearchScreen(MDScreen):
    def search_music(self, search_text: str):
        videos_list: MDList = self.ids.videos_list
        videos_list.clear_widgets()
        for song in YTMusic().search(search_text, filter="songs"):
            third_str = ""
            if song["year"]:
                third_str = f'Year: {song["year"]}, '
            if song["artists"]:
                artists = ", ".join(x["name"] for x in song["artists"])
                third_str = f"{third_str}Artists: {artists}"
            item = ThreeLineAvatarIconListItem(
                text=song["title"],
                secondary_text=f'Duration: {song["duration"]}',
                tertiary_text=third_str,
                on_release=self.open_song_dialog
            )
            item.details = song
            item.add_widget(
                ImageLeftWidgetWithoutTouch(source=song["thumbnails"][-1]["url"])
            )
            videos_list.add_widget(item)

    def open_song_dialog(self, item):
        song = item.details
        app = MDApp.get_running_app()
        #TODO: доделать dropdown + скачивание музыки
        app.dialog = MDDialog(
            title="Добавление в плейлист",
            type="custom",
            content_cls=SongDialog(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                ),
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                ),
            ],
        )
        app.dialog.open()
