from __future__ import unicode_literals
from pydub import AudioSegment
import youtube_dl
import os
import os.path
import subprocess
import shutil

__version__ = "0.1.0"

BANNER = r"""    ____________________________
  /|............................|
 | |:          Cassetter       :|
 | |:        Joss Moffatt      :|
 | |:     ,-.   _____   ,-.    :|
 | |:    ( `)) [_____] ( `))   :|
 |v|:     `-`   ' ' '   `-`    :|
 |||:     ,______________.     :|
 |||...../::::o::::::o::::\.....|
 |^|..../:::O::::::::::O:::\....|
 |/`---/--------------------`---|
 `.___/ /====/ /=//=/ /====/____/
      `--------------------'"""[1:]

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class MediaConverter(youtube_dl.YoutubeD):
    def __main__(self, options):
        super().__init__(options)
        self.options = options
        self.ids = []

    def convert_to_pcm(self, output_filename, start_time, end_time):
        output = subprocess.getoutput(['ffmpeg', '-i', 'download.wav',
                                      '-ss', str(start_time), '-to', str(end_time),
                                      output_filename])
        return output

    def download(self, url):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        video_id = self._get_id(url)

    def _get_id(self, url):
      if "youtube.com/watch?v=" in url:
        return re.replace('https://www.youtube.com/watch?v=', '')
      else:
        raise Exception('Currently only Youtube is supported.')

        
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
          

print(BANNER)
title = 'peter' #input("Enter Song Title")
file_format = 'mp3' #input("Enter codec")

# Join title and codec under PEP-8 convention
pcm_filename = '.'.join([title, 'wav'])
output_filename = '.'.join([title, file_format])

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'download.wav',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
'ffmpeg -i peter.wav out.wav'


t1 = 0
t2 = 60
convert_to_pcm(output_filename,t1,t2)
"""
audio_abs_path = os.path.abspath(pcm_filename)
newAudio = AudioSegment.from_wav(audio_abs_path)
newAudio = newAudio[t1:t2]
newAudio.export(output_filename, format=file_format) #Exports to a wav file in the current path.
"""

