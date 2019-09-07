from __future__ import unicode_literals
from omc import OnlineMediaConverter
import youtube_dl
import os
import os.path
import subprocess
import shutil
import configparser
import json


__version__ = "0.1.0"

BANNER = [r"""   ____________________________""",
r""" /|............................|""",
r"""| |:          Cassetter       :|""",
r"""| |:        Joss Moffatt      :|""",
r"""| |:     ,-.   _____   ,-.    :|""",
r"""| |:    ( `)) [_____] ( `))   :|""",
r"""|v|:     `-`   ' ' '   `-`    :|""",
r"""|||:     ,______________.     :|""",
r"""|||...../::::o::::::o::::\.....|""",
r"""|^|..../:::O::::::::::O:::\....|""",
r"""|/`---/--------------------`---|""",
r"""`.___/ /====/ /=//=/ /====/____/""",
r"""     `--------------------'"""]

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

def read_config():
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    extension = parser.get('DEFAULTS', 'EXTENSION')
    cache_limit = int(parser.get('DEFAULTS', 'CACHE_LIMIT'))
    return extension, cache_limit

def print_banner(banner_arr):
    longest_item_length = len(max(banner_arr, key=len))
    width = shutil.get_terminal_size()[0]
    offset = (width - longest_item_length) // 2
    for index, line in enumerate(banner_arr):
        print((" " * offset) + line )

def existing_file(filename):
    return os.path.isfile('media/' + filename)

def set_mapping(file_id, arr):
    with open('.cache/mappings.JSON', 'r') as f:
        mapping_dict = json.loads(f.read())
    mapping_dict[file_id] = arr
    with open('.cache/mappings.JSON', 'w') as f:
        f.write(json.dumps(mapping_dict))

def main():
    print_banner(BANNER)
    # Read in config varspo 
    extension, cache_limit = read_config()
    url = input("Enter Media URL > ")
    while True:
        title = input("Enter Desired Filename > ")
        output_filename = title + '.' + extension
        if not existing_file(output_filename):
            break
        else:
            print("This file already exists, try again")
    #TODO validate inputs
    print('Press [ENTER] to ignore clips')
    start_clip = input('Enter Start Timestamp for Clip > ')
    if len(start_clip) == 0:
        clip_times = ()
    else:
        end_clip = int(input('Enter End Timestamp for Clip > '))
        clip_times = (int(start_clip),end_clip)


    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'download.wav',
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    
    converter = OnlineMediaConverter(ydl_opts, extension, cache_limit)
    converter.download_from_url(url, output_filename, clip_times=clip_times)
    set_mapping(output_filename, [url, clip_times])
    


if __name__ == '__main__':
    main()


"""
'ffmpeg -i peter.wav out.wav'


t1 = 0
t2 = 60
convert_to_pcm(output_filename,t1,t2)

audio_abs_path = os.path.abspath(pcm_filename)
newAudio = AudioSegment.from_wav(audio_abs_path)
newAudio = newAudio[t1:t2]
newAudio.export(output_filename, format=file_format) #Exports to a wav file in the current path.
"""

