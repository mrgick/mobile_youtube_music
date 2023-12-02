from pathlib import Path

from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.screen import MDScreen


class SettingsScreen(MDScreen):
    def open_file_manager(self):
        self.file_manager = MDFileManager(
            select_path=self.select_path,
            preview=True,
        )
        app = MDApp.get_running_app()
        self.file_manager.show(str(app.music_path.absolute()))

    def select_path(self, path: str):
        app = MDApp.get_running_app()
        app.music_path = Path(path)
        self.file_manager.close()
        toast(str(app.music_path))
