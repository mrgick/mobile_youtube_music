# YT music app
Just a proof of concept that you can create a player app using kivy.


> Unfortunately I had to bring up an additional [api](https://github.com/mrgick/yt-dl-fast-api) to download mp3 files, as I couldn't get ffmpeg to work to convert from .webm to .mp3. But, you can try to build ffmpeg-kit with lame https://github.com/ArqiesAr/FFmpeg-Kit-Python


## Build android app
1. Download docker buildozer and build it 
```bash
git clone https://github.com/kivy/buildozer.git 
cd buildozer
docker build --tag=buildozer .
```

2. Build app
```bash
docker run --volume "$(pwd)":/home/user/hostcwd --volume "$HOME"/.buildozer:/home/user/.buildozer  buildozer android debug
```
## Screenshots
<details>
<summary>Screenshots of an app</summary>

![Search screen](screenshots/image1.png?raw=true "Search screen")
![Settings screen](screenshots/image4.png?raw=true "Settings screen")
![Playlists screen](screenshots/image3.png?raw=true "Playlists screen")
![Playlist detail screen](screenshots/image4.png?raw=true "Playlist detail screen")
![Player screen](screenshots/image5.png?raw=true "Player screen")

</details>