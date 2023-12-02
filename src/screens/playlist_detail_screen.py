from pathlib import Path

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import IconLeftWidgetWithoutTouch, MDList, OneLineIconListItem
from kivymd.uix.screen import MDScreen


class ConfirmationDialog(MDBoxLayout):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.message.text = text


class PlaylistDetailScreen(MDScreen):
    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        self.path = app.playlist_path
        self.refresh_list()

    def refresh_list(self):
        mdlist: MDList = self.ids.playlist_list
        mdlist.clear_widgets()
        for song in (
            x for x in self.path.iterdir() if x.is_file() and x.suffix == ".mp3"
        ):
            item = OneLineIconListItem(
                text=song.stem, on_release=self.delete_song_dialog
            )
            item.path = song
            item.add_widget(IconLeftWidgetWithoutTouch(icon="delete-outline"))
            mdlist.add_widget(item)

    def delete_song_dialog(self, item):
        self.confirm_dialog(
            f'Delete song "{item.path.stem}"?', self.delete_song, item.path
        )

    def delete_playlist_dialog(self):
        self.confirm_dialog(
            f'Delete playlist "{self.path.stem}"?', self.delete_playlist, self.path
        )

    def delete_playlist(self, path: Path):
        for child in path.glob("*"):
            child.unlink()
        path.rmdir()
        app = MDApp.get_running_app()
        app.dialog.dismiss()
        app.switch_screen("playlists_screen")

    def delete_song(self, path: Path):
        path.unlink()
        app = MDApp.get_running_app()
        self.refresh_list()
        app.dialog.dismiss()

    def confirm_dialog(self, text, ok_func, item):
        app = MDApp.get_running_app()
        app.dialog = MDDialog(
            title="Confirmation dialog",
            type="custom",
            content_cls=ConfirmationDialog(text),
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: ok_func(item),
                ),
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: app.dialog.dismiss(),
                ),
            ],
        )
        app.dialog.open()
