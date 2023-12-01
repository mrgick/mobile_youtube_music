from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem
from .playlists_screen import get_playlists
from utils.yt_api import get_metadata
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from PIL import Image as PilImage
from kivy.core.audio import SoundLoader


class ChoosePlaylistDialog(MDBoxLayout):
    def __init__(self, screen, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen = screen
        mdlist: MDList = self.ids.playlists_list
        for path in get_playlists():
            item = OneLineListItem(text=path.name, on_release=self.choosed_playlist)
            item.path = path
            mdlist.add_widget(item)

    def choosed_playlist(self, item):
        path = item.path
        print(path)
        self.screen.current_playlist = [
            x for x in path.iterdir() if x.is_file() and x.suffix == ".mp3"
        ]
        print(self.screen.current_playlist)
        if len(self.screen.current_playlist) >= 1:
            self.screen.current_music = 0
        else:
            self.screen.current_music = None
        self.screen.refresh(path.name)
        app = MDApp.get_running_app()
        app.dialog.dismiss()


class PlayerScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_playlist = None
        self.current_music = None
        self.sound = None

    def refresh(self, name):
        self.ids.playlist.text = name
        if self.current_music is not None:
            file = self.current_playlist[self.current_music]
            data = get_metadata(file)
            self.ids.track.text = (
                f'{data["title"]} by {data["artist"]} from {data["album"]}'
            )
            pil_image = PilImage.open(data["image"])
            kivy_texture = Texture.create(
                size=(pil_image.width, pil_image.height), colorfmt="rgba"
            )
            kivy_texture.blit_buffer(
                pil_image.tobytes(), colorfmt="rgb", bufferfmt="ubyte"
            )
            self.ids.art.texture = kivy_texture
            self.ids.art.reload()
            self.sound = SoundLoader().load(str(file))

    def play_pause_music(self):
        if self.sound and self.sound.state == 'stop':
            self.sound.play()
        elif self.sound and self.sound.state == 'play':
            self.sound.stop()

    def choose_playlist_dialog(self):
        app = MDApp.get_running_app()
        app.dialog = MDDialog(
            title="Create new playlist",
            type="custom",
            content_cls=ChoosePlaylistDialog(self),
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
