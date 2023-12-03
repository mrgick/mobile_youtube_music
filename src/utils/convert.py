#IMPORTING jnius
from jnius import autoclass
import time
from jnius import * 


#Declaring Variable so it can be used
FFMPEG = autoclass('com.sahib.pyff.ffpy')

def convert(song, dir_path):
    #EXECUTED FFMPEG COMMAND, COMMAND IS STRING
    audio_in = str(dir_path / (song['title'] + '.webm'))
    audio_out = str(dir_path / (song['title'] + '.mp3'))
    ffmpeg_command = f"-i '{audio_in}' -vn -acodec libmp3lame '{audio_out}'"
    ffmpegCommand = FFMPEG.Run(ffmpeg_command)

    #PRINTS RETURN (OUTPUT OF THE COMMAND)
    print(ffmpegCommand)
    time.sleep(10)
