import io
from pathlib import Path

import requests
import yt_dlp
from mutagen.id3 import APIC, ID3, TALB, TIT2, TPE1
from ytmusicapi import YTMusic

yt_searcher = YTMusic()


def search_music(search_text: str) -> list[dict]:
    return yt_searcher.search(search_text, filter="songs")


def download_music(song: dict, dir_path: Path, progress_hook):
    options = {
        "format": "bestaudio/best",
        "outtmpl": str(dir_path / (song["title"] + ".%(ext)s")),
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
    audiofile = ID3(dir_path / f"{song['title']}.mp3")

    audiofile.add(TIT2(encoding=3, text=song["title"]))

    if song["artists"]:
        audiofile.add(
            TPE1(encoding=3, text=", ".join(x["name"] for x in song["artists"]))
        )

    if song["album"]:
        audiofile.add(TALB(encoding=3, text=song["album"]["name"]))

    response = requests.get(song["thumbnails"][-1]["url"]).content
    audiofile.add(APIC(3, mime="image/jpeg", type=3, desc="", data=response))

    audiofile.save(v2_version=3)


def get_metadata(file_path: Path) -> dict:
    audiofile = ID3(file_path)
    info = {
        "title": audiofile.get("TIT2").text[0] if "TIT2" in audiofile else None,
        "artist": audiofile.get("TPE1").text[0] if "TPE1" in audiofile else None,
        "album": audiofile.get("TALB").text[0] if "TALB" in audiofile else None,
        "image": None,
    }

    if not info["title"]:
        info["title"] = file_path.stem
    #print(audiofile)
    if "APIC:" in audiofile:
        image_data = audiofile.get("APIC:").data
        info["image"] = io.BytesIO(image_data)

    return info
