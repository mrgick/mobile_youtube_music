from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from pathlib import Path

def get_playlists() -> list[Path]:
    app = MDApp.get_running_app()
    return [x for x in app.music_path.iterdir() if x.is_dir()]

class CreatePlaylistDialog(MDBoxLayout):
    def create_playlist(self, playlist_name: str):
        app = MDApp.get_running_app()
        new_dir: Path = app.music_path / playlist_name
        new_dir.mkdir(exist_ok=True)
        tf: MDTextField = self.ids.name
        tf.text = f'Created playlist "{playlist_name}"'
        tf.disabled = True
        btn: MDFlatButton = self.ids.btn
        btn.disabled = True

class PlaylistsScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh_list()

    def refresh_list(self):
        mdlist: MDList = self.ids.playlist_list
        mdlist.clear_widgets()
        for path in get_playlists():
            item = OneLineListItem(text=path.name)
            mdlist.add_widget(item)

    def open_playlist(self, playlist):
        pass # TODO: playlist screen detail

    def add_playlist(self):
        app = MDApp.get_running_app()
        app.dialog = MDDialog(
            title='Create new playlist',
            type="custom",
            content_cls=CreatePlaylistDialog(),
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.close_dialog(app),
                ),
            ],
        )
        app.dialog.open()

    def close_dialog(self, app):
        self.refresh_list()
        app.dialog.dismiss()
