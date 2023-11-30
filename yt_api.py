from ytmusicapi import YTMusic
from pathlib import Path
import yt_dlp
import eyed3
import requests

yt_searcher = YTMusic()


def search_music(search_text: str) -> list[dict]:
    return yt_searcher.search(search_text, filter="songs")


def download_music(song: dict, dir_path: Path, progress_hook):
    options = {
        "format": "bestaudio/best",
        "outtmpl": str(dir_path / "%(title)s.%(ext)s"),
        "progress_hooks": [progress_hook],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "0",
            }
        ],
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={song['videoId']}"])


def add_metadata(song: dict, dir_path: Path):
    audiofile = eyed3.load(dir_path / f"{song['title']}.mp3")

    audiofile.tag.title = song["title"]
    if song["artists"]:
        audiofile.tag.artist = ", ".join(x["name"] for x in song["artists"])
    if song["album"]:
        audiofile.tag.album = song["album"]["name"]

    response = requests.get(song["thumbnails"][-1]["url"]).content
    audiofile.tag.images.set(3, response, "image/jpeg")

    audiofile.tag.save()
