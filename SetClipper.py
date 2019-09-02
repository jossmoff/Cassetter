from __future__ import unicode_literals
from pydub import AudioSegment
import youtube_dl
import os

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


title = 'peter' #input("Enter Song Title")
file_format = 'mp3' #input("Enter codec")

# Join title and codec under PEP-8 convention
filename = '.'.join([title, 'wav'])

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': filename,
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}


with youtube_dl.YoutubeDL(ydl_opts) as ydl:
  ydl.download(['www.youtube.com/watch?v=hm6COzCAQhg'])

t1 = 0 * 1000 #Works in milliseconds
t2 = 60 * 1000
audio_abs_path = os.path.abspath("peter.wav")
newAudio = AudioSegment.from_wav(audio_abs_path)
newAudio = newAudio[t1:t2]
newAudio.export(filename, format=file_format) #Exports to a wav file in the current path.


