from kivy.core.audio import SoundLoader
from kivy.graphics.texture import Texture
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.screen import MDScreen
from PIL import Image, ImageFilter

from utils.yt_api import get_metadata

from .playlists_screen import get_playlists


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
        self.screen.current_playlist = [
            x for x in path.iterdir() if x.is_file() and x.suffix == ".mp3"
        ]
        self.screen.refresh(path.name)
        app = MDApp.get_running_app()
        app.dialog.dismiss()


class PlayerScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_playlist = None
        self.current_music = None
        self.sound = None
        self.play_next = False

    def choose_music(self, number: int = 0):
        if self.sound:
            self.sound.stop()
            self.sound.unload()
        if not self.current_playlist or len(self.current_playlist) == 0:
            return None
        if number < 0:
            self.current_music = len(self.current_playlist) - 1
        elif number > len(self.current_playlist) - 1:
            self.current_music = 0
        else:
            self.current_music = number
        file = self.current_playlist[self.current_music]
        data = get_metadata(file)
        track = data["title"]
        if data["artist"]:
            track += f' by {data["artist"]}'
        if data["album"]:
            track += f' from {data["album"]}'
        self.ids.track.text = track
        kivy_texture = None
        if data["image"]:
            pil_image = Image.open(data["image"])
            pil_image = (
                pil_image.resize((360, 360))
                .filter(ImageFilter.BoxBlur(radius=1))
                .rotate(180)
            )
            kivy_texture = Texture.create(
                size=(pil_image.width, pil_image.height), colorfmt="rgba"
            )
            kivy_texture.blit_buffer(
                pil_image.tobytes(), colorfmt="rgb", bufferfmt="ubyte"
            )
        self.ids.art.texture = kivy_texture
        self.sound = SoundLoader().load(str(file))
        self.sound.bind(on_stop=self.player_stop)

    def refresh(self, name):
        self.ids.playlist.text = name
        self.choose_music(0)

    def player_stop(self, instance):
        if self.play_next:
            self.choose_music(self.current_music + 1)
            self.sound.play()

    def play_pause_music(self):
        if self.sound and self.sound.state == "stop":
            self.play_next = True
            self.sound.play()
        elif self.sound and self.sound.state == "play":
            self.play_next = False
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
